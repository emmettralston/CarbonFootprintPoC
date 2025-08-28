from fastapi import Header, HTTPException


async def get_org_id(x_org_id: int | None = Header(default=None)) -> int:
    """Temporary org scoping via header for PoC.
    In production, derive org_id from JWT.
    """
    if x_org_id is None:
        raise HTTPException(status_code=400, detail="X-Org-Id header required")
    return x_org_id