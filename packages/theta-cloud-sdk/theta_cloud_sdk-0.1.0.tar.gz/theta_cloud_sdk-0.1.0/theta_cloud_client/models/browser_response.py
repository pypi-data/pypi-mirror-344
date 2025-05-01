from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="BrowserResponse")


@_attrs_define
class BrowserResponse:
    """
    Attributes:
        id (str):
        ws_url_http_endpoint (str):
        vnc_url (str):
    """

    id: str
    ws_url_http_endpoint: str
    vnc_url: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        ws_url_http_endpoint = self.ws_url_http_endpoint

        vnc_url = self.vnc_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "ws_url_http_endpoint": ws_url_http_endpoint,
                "vnc_url": vnc_url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        # normalize field names from JSON (camelCase to snake_case)
        if "wsUrl_http_endpoint" in d and "ws_url_http_endpoint" not in d:
            d["ws_url_http_endpoint"] = d.pop("wsUrl_http_endpoint")
        if "vncUrl" in d and "vnc_url" not in d:
            d["vnc_url"] = d.pop("vncUrl")
        id = d.pop("id")

        ws_url_http_endpoint = d.pop("ws_url_http_endpoint")

        vnc_url = d.pop("vnc_url")

        browser_response = cls(
            id=id,
            ws_url_http_endpoint=ws_url_http_endpoint,
            vnc_url=vnc_url,
        )

        browser_response.additional_properties = d
        return browser_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
