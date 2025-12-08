from typing import Optional
from pydantic import BaseModel, Field
from decimal import Decimal, ROUND_HALF_UP

from pydantic_settings import BaseSettings


class DiscogsSettings(BaseSettings):
    access_token: Optional[str] = None

    class Config:
        env_prefix = "DISCOGS_"


class DiscogsPrice(BaseModel):
    currency: str
    value: Decimal


class DiscogsPriceSuggestions(BaseModel):
    mint: Optional[DiscogsPrice] = Field(None, alias="Mint (M)")
    near_mint: Optional[DiscogsPrice] = Field(None, alias="Near Mint (NM or M-)")
    vg_plus: Optional[DiscogsPrice] = Field(None, alias="Very Good Plus (VG+)")
    vg: Optional[DiscogsPrice] = Field(None, alias="Very Good (VG)")
    g_plus: Optional[DiscogsPrice] = Field(None, alias="Good Plus (G+)")
    g: Optional[DiscogsPrice] = Field(None, alias="Good (G)")
    fair: Optional[DiscogsPrice] = Field(None, alias="Fair (F)")
    poor: Optional[DiscogsPrice] = Field(None, alias="Poor (P)")

    class Config:
        validate_by_name = True

    def return_price_based_on_quality_vs_price(self) -> float:
        if self.g_plus:
            return float(
                self.g_plus.value.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
            )

        if self.vg_plus:
            return float(
                self.vg_plus.value.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
            )

        if self.near_mint:
            return float(
                self.near_mint.value.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
            )

        if self.mint:
            return float(
                self.mint.value.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
            )

        if self.vg:
            return float(
                self.vg.value.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
            )

        return 0.0
