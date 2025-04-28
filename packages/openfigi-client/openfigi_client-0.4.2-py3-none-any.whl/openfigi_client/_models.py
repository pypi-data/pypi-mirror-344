import datetime as dt
import enum
from typing import Annotated, Any, Literal

import msgspec

Key = Literal[
    "idType",
    "exchCode",
    "micCode",
    "currency",
    "marketSecDes",
    "securityType",
    "securityType2",
    "stateCode",
]


class IdType(enum.Enum):
    """Supported ID types for OpenFIGI API."""

    ID_ISIN = "ID_ISIN"
    ID_BB_UNIQUE = "ID_BB_UNIQUE"
    ID_SEDOL = "ID_SEDOL"
    ID_COMMON = "ID_COMMON"
    ID_WERTPAPIER = "ID_WERTPAPIER"
    ID_CUSIP = "ID_CUSIP"
    ID_BB = "ID_BB"
    ID_ITALY = "ID_ITALY"
    ID_EXCH_SYMBOL = "ID_EXCH_SYMBOL"
    ID_FULL_EXCHANGE_SYMBOL = "ID_FULL_EXCHANGE_SYMBOL"
    COMPOSITE_ID_BB_GLOBAL = "COMPOSITE_ID_BB_GLOBAL"
    ID_BB_GLOBAL_SHARE_CLASS_LEVEL = "ID_BB_GLOBAL_SHARE_CLASS_LEVEL"
    ID_BB_SEC_NUM_DES = "ID_BB_SEC_NUM_DES"
    ID_BB_GLOBAL = "ID_BB_GLOBAL"
    TICKER = "TICKER"
    ID_CUSIP_8_CHR = "ID_CUSIP_8_CHR"
    OCC_SYMBOL = "OCC_SYMBOL"
    UNIQUE_ID_FUT_OPT = "UNIQUE_ID_FUT_OPT"
    OPRA_SYMBOL = "OPRA_SYMBOL"
    TRADING_SYSTEM_IDENTIFIER = "TRADING_SYSTEM_IDENTIFIER"
    ID_CINS = "ID_CINS"
    ID_SHORT_CODE = "ID_SHORT_CODE"
    BASE_TICKER = "BASE_TICKER"
    VENDOR_INDEX_CODE = "VENDOR_INDEX_CODE"


NullableNumberInterval = list[int | float | None]
NullableDateInterval = list[dt.date | None]


def validate_nullable_number_interval(v: NullableNumberInterval) -> None:
    """Validate the input value."""
    if not isinstance(v, list):
        raise TypeError("List required")

    if len(v) != 2:  # noqa: PLR2004
        raise TypeError("The list must contain two elements")

    if not isinstance(v[0], int | float | None) or not isinstance(
        v[1],
        int | float | None,
    ):
        raise TypeError("Elements must be of type int, float or None")

    if v[0] is None and v[1] is None:
        raise TypeError("At least one element must be a number")

    if v[0] is not None and v[1] is not None and v[0] > v[1]:
        raise TypeError("Numbers must be sorted in ascending order")


def validate_nullable_date_interval(v: NullableDateInterval) -> None:
    """Validate the input value."""
    if not isinstance(v, list):
        raise TypeError("List required")

    if len(v) != 2:  # noqa: PLR2004
        raise TypeError("The list must contain two elements")

    if not isinstance(v[0], dt.date | None) or not isinstance(v[1], dt.date | None):
        raise TypeError("Elements must be of type date or None")

    if v[0] is None and v[1] is None:
        raise TypeError("At least one element must be a date")

    if v[0] is not None and v[1] is not None and v[0] + dt.timedelta(days=365) < v[1]:
        raise TypeError("Dates must not be more than a year apart")


class Model(msgspec.Struct):
    """BaseModel configured for OpenFIGI models."""

    def validate(self) -> None:
        """Validate self."""
        # workaround to achieve validation on initialization
        # the dynamic model will validate the field types, but won't have
        # the __post_init__ method. If we just used self, we'd get infinite
        # recursion
        SelfModel = msgspec.defstruct(  # noqa: N806
            "SelfModel",
            [
                (field.encode_name, field.type, field.default)
                for field in msgspec.structs.fields(self)
            ],
        )
        msgspec.json.decode(self.to_json(), type=SelfModel)

    def to_dict(self, *, by_alias: bool = False) -> dict[str, Any]:
        """Return the model as a dictionary."""
        return {
            field.encode_name if by_alias else field.name: getattr(self, field.name)
            for field in msgspec.structs.fields(self)
        }

    def to_json(self) -> bytes:
        """Return the model as a JSON string."""
        return msgspec.json.encode(self)


class MappingJob(Model, omit_defaults=True, kw_only=True):
    """MappingJob implementation using custom validators."""

    id_type: IdType = msgspec.field(name="idType")
    id_value: str | int = msgspec.field(name="idValue")
    exch_code: str | None = msgspec.field(default=None, name="exchCode")
    mic_code: str | None = msgspec.field(default=None, name="micCode")
    currency: str | None = None
    market_sec_des: str | None = msgspec.field(default=None, name="marketSecDes")
    security_type: str | None = msgspec.field(default=None, name="securityType")
    security_type_2: str | None = msgspec.field(default=None, name="securityType2")
    include_unlisted_equities: bool | None = msgspec.field(
        default=None,
        name="includeUnlistedEquities",
    )
    option_type: str | None = msgspec.field(default=None, name="optionType")
    strike: NullableNumberInterval | None = None
    contract_size: NullableNumberInterval | None = msgspec.field(
        default=None,
        name="contractSize",
    )
    coupon: NullableNumberInterval | None = None
    expiration: NullableDateInterval | None = None
    maturity: NullableDateInterval | None = None
    state_code: str | None = msgspec.field(default=None, name="stateCode")

    def __post_init__(self) -> None:
        """Post-initialization method."""
        self.validate()
        self_dict = self.to_dict()

        self.required_for_some_id_types(self.security_type_2, self_dict)
        self.required_for_some_security_type_2(self.expiration, self_dict)
        self.required_for_pool(self.maturity, self_dict)

        for field in ("strike", "contract_size", "coupon"):
            if value := self_dict.get(field):
                validate_nullable_number_interval(value)
        for field in ("expiration", "maturity"):
            if value := self_dict.get(field):
                validate_nullable_date_interval(value)

    @classmethod
    def required_for_some_id_types(cls, v: str | None, values: dict[str, Any]) -> None:
        """Validate the security_type_2 field."""
        id_type = (
            values["id_type"].value
            if isinstance(values["id_type"], IdType)
            else values["id_type"]
        )
        if (
            id_type in [IdType.BASE_TICKER.value, IdType.ID_EXCH_SYMBOL.value]
            and v is None
        ):
            raise ValueError(
                "Field security_type_2 is mandatory when id_type is 'BASE_TICKER' or 'ID_EXCH_SYMBOL'",
            )

    @classmethod
    def required_for_some_security_type_2(
        cls,
        v: NullableDateInterval | None,
        values: dict[str, Any],
    ) -> None:
        """Validate the expiration field."""
        if (
            "security_type_2" in values
            and values["security_type_2"] in ["Option", "Warrant"]
            and v is None
        ):
            raise ValueError(
                "Field expiration is mandatory when security_type_2 is 'Option' or 'Warrant'",
            )

    @classmethod
    def required_for_pool(
        cls,
        v: NullableDateInterval | None,
        values: dict[str, Any],
    ) -> None:
        """Validate the maturity field."""
        if (
            "security_type_2" in values
            and values["security_type_2"] == "Pool"
            and v is None
        ):
            raise ValueError(
                "Field maturity is mandatory when security_type_2 is 'Pool'",
            )


BulkMappingJob = list[MappingJob]


class FigiResult(Model):
    """A Figi mapping result."""

    figi: str | None
    security_type: str | None = msgspec.field(name="securityType")
    market_sector: str | None = msgspec.field(name="marketSector")
    ticker: str | None
    name: str | None
    exch_code: str | None = msgspec.field(name="exchCode")
    share_class_figi: str | None = msgspec.field(name="shareClassFIGI")
    composite_figi: str | None = msgspec.field(name="compositeFIGI")
    security_type2: str | None = msgspec.field(name="securityType2")
    security_description: str | None = msgspec.field(name="securityDescription")
    metadata: str | None = None


class MappingJobResultFigiList(Model, tag="ok"):
    """Contains the list of Figi mapping results."""

    data: list[FigiResult]


class MappingJobResultFigiNotFound(Model, tag="warning"):
    """Contains the warning message for Figi not found."""

    warning: str


class MappingJobResultError(Model, tag="error"):
    """Contains the error message for invalid MappingJob."""

    error: str


MappingJobResult = (
    MappingJobResultFigiList | MappingJobResultFigiNotFound | MappingJobResultError
)


QueryField = Annotated[str, msgspec.Meta(min_length=1)]


class Filter(Model, omit_defaults=True, kw_only=True):
    """Search/Filter query object."""

    query: QueryField | None = None
    start: str | None = None
    exch_code: str | None = msgspec.field(default=None, name="exchCode")
    mic_code: str | None = msgspec.field(default=None, name="micCode")
    currency: str | None = None
    market_sec_des: str | None = msgspec.field(default=None, name="marketSecDes")
    security_type: str | None = msgspec.field(default=None, name="securityType")
    security_type_2: str | None = msgspec.field(default=None, name="securityType2")
    include_unlisted_equities: bool | None = msgspec.field(
        default=None,
        name="includeUnlistedEquities",
    )
    option_type: str | None = msgspec.field(default=None, name="optionType")
    strike: NullableNumberInterval | None = None
    contract_size: NullableNumberInterval | None = msgspec.field(
        default=None,
        name="contractSize",
    )
    coupon: NullableNumberInterval | None = None
    expiration: NullableDateInterval | None = None
    maturity: NullableDateInterval | None = None
    state_code: str | None = msgspec.field(default=None, name="stateCode")

    def __post_init__(self) -> None:
        """Post-initialization method."""
        self.validate()
        self_dict = self.to_dict()

        if all(v is None for v in self_dict.values()):
            raise ValueError("At least one field must be provided")

        self.required_for_some_security_type_2(self.expiration, self_dict)
        self.required_for_pool(self.maturity, self_dict)

        for field in ("strike", "contract_size", "coupon"):
            if value := self_dict.get(field):
                validate_nullable_number_interval(value)
        for field in ("expiration", "maturity"):
            if value := self_dict.get(field):
                validate_nullable_date_interval(value)

    @classmethod
    def required_for_some_security_type_2(
        cls,
        v: NullableDateInterval | None,
        values: dict[str, Any],
    ) -> None:
        """Validate the expiration field."""
        if (
            "security_type_2" in values
            and values["security_type_2"] in ["Option", "Warrant"]
            and v is None
        ):
            raise ValueError(
                "Field expiration is mandatory when security_type_2 is 'Option' or 'Warrant'",
            )

    @classmethod
    def required_for_pool(
        cls,
        v: NullableDateInterval | None,
        values: dict[str, Any],
    ) -> None:
        """Validate the maturity field."""
        if (
            "security_type_2" in values
            and values["security_type_2"] == "Pool"
            and v is None
        ):
            raise ValueError(
                "Field maturity is mandatory when security_type_2 is 'Pool'",
            )
