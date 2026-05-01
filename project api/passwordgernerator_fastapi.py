import secrets
import string
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, validator

app = FastAPI(
    title="Password Generator API",
    description="A secure password generator built with FastAPI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ──────────────────────────────────────────────
# Schemas
# ──────────────────────────────────────────────

class PasswordRequest(BaseModel):
    length: int = Field(default=16, ge=4, le=128, description="Password length (4–128)")
    use_uppercase: bool = Field(default=True, description="Include uppercase letters A-Z")
    use_lowercase: bool = Field(default=True, description="Include lowercase letters a-z")
    use_digits: bool = Field(default=True, description="Include digits 0-9")
    use_symbols: bool = Field(default=True, description="Include special characters")
    exclude_ambiguous: bool = Field(default=False, description="Exclude ambiguous chars (O, 0, l, 1, I)")
    quantity: int = Field(default=1, ge=1, le=20, description="Number of passwords to generate (max 20)")

    @validator("use_uppercase", "use_lowercase", "use_digits", "use_symbols", always=True)
    def at_least_one_charset(cls, v, values):
        return v  # checked in route below


class PasswordResponse(BaseModel):
    passwords: list[str]
    length: int
    strength: str
    entropy_bits: float
    charset_size: int


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

AMBIGUOUS = set("O0lI1|`'\"")

def build_charset(req: PasswordRequest) -> str:
    charset = ""
    if req.use_uppercase:
        charset += string.ascii_uppercase
    if req.use_lowercase:
        charset += string.ascii_lowercase
    if req.use_digits:
        charset += string.digits
    if req.use_symbols:
        charset += string.punctuation

    if req.exclude_ambiguous:
        charset = "".join(c for c in charset if c not in AMBIGUOUS)

    return charset


def calculate_strength(entropy: float) -> str:
    if entropy < 28:
        return "Very Weak"
    elif entropy < 36:
        return "Weak"
    elif entropy < 60:
        return "Moderate"
    elif entropy < 128:
        return "Strong"
    else:
        return "Very Strong"


def generate_password(charset: str, length: int) -> str:
    """Cryptographically secure password generation."""
    return "".join(secrets.choice(charset) for _ in range(length))


# ──────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def serve_ui():
    with open("index.html", "r") as f:
        return f.read()


@app.post("/generate", response_model=PasswordResponse, summary="Generate passwords")
async def generate_passwords(req: PasswordRequest):
    """
    Generate one or more cryptographically secure passwords.

    - **length**: total character count
    - **use_uppercase / lowercase / digits / symbols**: character sets to include
    - **exclude_ambiguous**: removes chars like O, 0, l, 1 that look similar
    - **quantity**: how many passwords to return (1–20)
    """
    charset = build_charset(req)

    if not charset:
        raise HTTPException(
            status_code=422,
            detail="At least one character set must be selected."
        )

    import math
    entropy = req.length * math.log2(len(charset))
    strength = calculate_strength(entropy)

    passwords = [generate_password(charset, req.length) for _ in range(req.quantity)]

    return PasswordResponse(
        passwords=passwords,
        length=req.length,
        strength=strength,
        entropy_bits=round(entropy, 2),
        charset_size=len(charset)
    )


@app.get("/health", summary="Health check")
async def health():
    return {"status": "ok", "service": "Password Generator API"}