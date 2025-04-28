import asyncio
import logging
import time
import urllib.parse
from typing import Any, cast

import httpx
import msgspec

from openfigi_client._models import (
    FigiResult,
    Filter,
    Key,
    MappingJob,
    MappingJobResult,
)
from openfigi_client.exceptions import (
    FilterQueryError,
    HTTPError,
    TooManyMappingJobsError,
)

logger = logging.getLogger(__name__)


class OpenFigiBase:
    """OpenFigi base client."""

    BASE_URL = "https://api.openfigi.com"
    MAX_MAPPING_REQUESTS_NO_KEY = 25
    MAX_MAPPING_JOBS_NO_KEY = 10
    MAX_SEARCH_REQUESTS_NO_KEY = 5
    MAX_MAPPING_REQUESTS_KEY = 250
    MAX_MAPPING_JOBS_KEY = 100
    MAX_SEARCH_REQUESTS_KEY = 20

    def __init__(self, api_key: str | None = None, version: int = 3) -> None:
        """
        Providing an API key allows for improved rate limitations.

        Args:
            api_key: Optional API key.
            version: OpenFIGI API version to use.
        """
        self._api_key = api_key
        self._version = version
        self._json_decoder = msgspec.json.Decoder()
        self._json_encoder = msgspec.json.Encoder()

    def url(self, endpoint: str) -> str:
        """The base URL for the OpenFIGI API."""
        return urllib.parse.urljoin(self.BASE_URL, f"v{self._version}/{endpoint}")

    @property
    def max_mapping_requests(self) -> int:
        """
        The maximum number of mapping requests per minute depends on whether an API key was provided or not.

        Returns:
            The maximum number of mapping requests per minute
        """
        return (
            self.MAX_MAPPING_REQUESTS_KEY
            if self._api_key
            else self.MAX_MAPPING_REQUESTS_NO_KEY
        )

    @property
    def max_mapping_jobs(self) -> int:
        """
        The maximum number of mapping jobs per request depends on whether an API key was provided or not.

        Returns:
            The maximum number of mapping jobs per request
        """
        return (
            self.MAX_MAPPING_JOBS_KEY if self._api_key else self.MAX_MAPPING_JOBS_NO_KEY
        )

    @property
    def max_search_requests(self) -> int:
        """
        The maximum number of search/filter requests per minute depends on whether an API key was provided or not.

        Returns:
            The maximum number of search/filter requests per minute
        """
        return (
            self.MAX_SEARCH_REQUESTS_KEY
            if self._api_key
            else self.MAX_SEARCH_REQUESTS_NO_KEY
        )

    @property
    def headers(self) -> dict[str, str]:
        """
        Build the HTTP headers for all endpoints depending on whether an API key was provided or not.

        Returns:
            A dictionary of HTTP headers
        """
        content_type = {"Content-Type": "application/json"}
        authorization = {"X-OPENFIGI-APIKEY": self._api_key} if self._api_key else {}
        return content_type | authorization

    def _validate_mapping_jobs(self, mapping_jobs: list[MappingJob]) -> None:
        """Make sure the number of MappingJobs does not exceed the maximum allowed."""
        if len(mapping_jobs) > self.max_mapping_jobs:
            msg = (
                f"The maximum number of MappingJobs "
                f"{'with' if self._api_key else 'without'} API key "
                f"is {self.max_mapping_jobs} per request"
            )
            raise TooManyMappingJobsError(msg)

    def _process_mapping_results(self, result: bytes) -> list[MappingJobResult]:
        """Process the mapping results."""
        decoded_result: list[dict[str, Any]] = self._json_decoder.decode(result)
        results = []
        for job_result in decoded_result:
            if "data" in job_result:
                type_ = "ok"
            elif "warning" in job_result:
                type_ = "warning"
            elif "error" in job_result:
                type_ = "error"
            else:
                raise ValueError("Unexpected result type")
            results.append({"type": type_, **job_result})

        return msgspec.convert(results, type=list[MappingJobResult])

    def _process_filter_result(self, result: dict[str, Any]) -> list[FigiResult]:
        """Process the filter results."""
        if "error" in result:
            raise FilterQueryError(result["error"])
        return msgspec.convert(result["data"], type=list[FigiResult])


class OpenFigiSync(OpenFigiBase):
    """OpenFigi API client."""

    def map(self, mapping_jobs: list[MappingJob]) -> list[MappingJobResult]:
        """
        Map third party identifiers to FIGIs.

        The number of mapping jobs is limited (the rate limit depends on whether an API key was provided or not).

        A MappingJobResult can be either:
            - a MappingJobResultFigiList in case results were found for the given MappingJob request
            - a MappingJobResultFigiNotFound in case nothing was found
            - a MappingJobResultError in case the MappingJob was invalid (should not happen with validation)

        The MappingJobResult at index i contains the results for the MappingJob at index i in the request.

        Args:
            mapping_jobs: a list of MappingJob objects

        Returns:
            A list of MappingJobResult objects
        """
        self._validate_mapping_jobs(mapping_jobs)
        result = self._request(
            method="POST",
            url=self.url("mapping"),
            data=self._json_encoder.encode(mapping_jobs),
            headers=self.headers,
        ).content
        return self._process_mapping_results(result)

    def get_id_types(self) -> list[str]:
        """
        Get the list of possible values for `id_type`.

        Returns:
            The list of possible values for `id_type`
        """
        return self._get_values("idType")

    def get_exch_codes(self) -> list[str]:
        """
        Get the list of possible values for `exch_code`.

        Returns:
            The list of possible values for `exch_code`
        """
        return self._get_values("exchCode")

    def get_mic_codes(self) -> list[str]:
        """
        Get the list of possible values for `mic_code`.

        Returns:
            The list of possible values for `mic_code`
        """
        return self._get_values("micCode")

    def get_currencies(self) -> list[str]:
        """
        Get the list of possible values for `currency`.

        Returns:
            The list of possible values for `currency`
        """
        return self._get_values("currency")

    def get_market_sec_des(self) -> list[str]:
        """
        Get the list of possible values for `market_sec_des`.

        Returns:
            The list of possible values for `market_sec_des`
        """
        return self._get_values("marketSecDes")

    def get_security_types(self) -> list[str]:
        """
        Get the list of possible values for `security_type`.

        Returns:
            The list of possible values for `security_type`
        """
        return self._get_values("securityType")

    def get_security_types_2(self) -> list[str]:
        """
        Get the list of possible values for `security_type_2`.

        Returns:
            The list of possible values for `security_type_2`
        """
        return self._get_values("securityType2")

    def get_state_codes(self) -> list[str]:
        """
        Get the list of possible values for `state_code`.

        Returns:
            The list of possible values for `state_code`
        """
        return self._get_values("stateCode")

    def _get_values(self, key: Key) -> list[str]:
        """
        Get the current list of values for the enum-like properties on Mapping Jobs.

        Returns:
            The list of possible values for the requested field
        """
        url = self.url(f"mapping/values/{key}")
        result = self._request(method="GET", url=url, headers=self.headers)
        values = self._json_decoder.decode(result.content)["values"]
        return cast("list[str]", values)

    def filter(self, query: Filter, timeout: int | None = 60) -> list[FigiResult]:
        """
        Search for FIGIs using keywords and other filters.

        The results are listed alphabetically by FIGI and include the total number of results.

        Args:
            query: Query object
            timeout: The maximum time in seconds to wait for the results to be fetched

        Returns:
            list: a list of FigiResult objects
        """
        start = time.time()

        # Requests rate limitation for Search/Filter API
        # We add half a second extra
        delay = 60 / self.max_search_requests + 0.5

        url = self.url("filter")
        headers = self.headers
        data = self._json_encoder.encode(query)
        result = self._json_decoder.decode(
            self._request(
                method="POST",
                url=url,
                data=data,
                headers=headers,
                timeout=timeout,
            ).content,
        )

        mapping_job_results = self._process_filter_result(result)

        while "next" in result:
            time.sleep(delay)
            query.start = result["next"]
            data = self._json_encoder.encode(query)
            result = self._json_decoder.decode(
                self._request(
                    method="POST",
                    url=url,
                    data=data,
                    headers=headers,
                    timeout=timeout,
                ).content,
            )
            mapping_job_results += self._process_filter_result(result)
            if timeout is not None and time.time() - start > timeout:
                logger.warning(
                    "Call timed out. Latest `next` value: %s",
                    result["next"],
                )
                break

        return mapping_job_results

    def get_total_number_of_matches(self, query: Filter) -> int:
        """
        Return the total number of matches for a given query.

        The function only makes one call to the `filter` endpoint and returns the `total` field
        from the response.

        Args:
            query: Filter object

        Returns:
            The total number of matches as a positive integer
        """
        result = self._json_decoder.decode(
            self._request(
                method="POST",
                url=self.url("filter"),
                data=self._json_encoder.encode(query),
                headers=self.headers,
            ).content,
        )
        return cast("int", result["total"])

    @staticmethod
    def _request(
        method: str,
        url: str,
        headers: dict[str, str],
        data: bytes | None = None,
        timeout: int | None = None,
    ) -> httpx.Response:
        """
        Make remote call.

        Raises:
            HTTPError: A custom exception in case of HTTP error.
        """
        with httpx.Client() as client:
            response = client.request(
                method=method,
                url=url,
                headers=headers,
                content=data,
                timeout=timeout,
            )

        if response.status_code != httpx.codes.OK:
            raise HTTPError(response.status_code, response.text)

        return response


class OpenFigiAsync(OpenFigiBase):
    """OpenFigi async API client."""

    async def map(self, mapping_jobs: list[MappingJob]) -> list[MappingJobResult]:
        """
        Map third party identifiers to FIGIs.

        The number of mapping jobs is limited (the rate limit depends on whether an API key was provided or not).

        A MappingJobResult can be either:
            - a MappingJobResultFigiList in case results were found for the given MappingJob request
            - a MappingJobResultFigiNotFound in case nothing was found
            - a MappingJobResultError in case the MappingJob was invalid (should not happen with validation)

        The MappingJobResult at index i contains the results for the MappingJob at index i in the request.

        Args:
            mapping_jobs: a list of MappingJob objects

        Returns:
            A list of MappingJobResult objects
        """
        self._validate_mapping_jobs(mapping_jobs)
        result = (
            await self._request(
                method="POST",
                url=self.url("mapping"),
                data=self._json_encoder.encode(mapping_jobs),
                headers=self.headers,
            )
        ).content
        return self._process_mapping_results(result)

    async def get_id_types(self) -> list[str]:
        """
        Get the list of possible values for `id_type`.

        Returns:
            The list of possible values for `id_type`
        """
        return await self._get_values("idType")

    async def get_exch_codes(self) -> list[str]:
        """
        Get the list of possible values for `exch_code`.

        Returns:
            The list of possible values for `exch_code`
        """
        return await self._get_values("exchCode")

    async def get_mic_codes(self) -> list[str]:
        """
        Get the list of possible values for `mic_code`.

        Returns:
            The list of possible values for `mic_code`
        """
        return await self._get_values("micCode")

    async def get_currencies(self) -> list[str]:
        """
        Get the list of possible values for `currency`.

        Returns:
            The list of possible values for `currency`
        """
        return await self._get_values("currency")

    async def get_market_sec_des(self) -> list[str]:
        """
        Get the list of possible values for `market_sec_des`.

        Returns:
            The list of possible values for `market_sec_des`
        """
        return await self._get_values("marketSecDes")

    async def get_security_types(self) -> list[str]:
        """
        Get the list of possible values for `security_type`.

        Returns:
            The list of possible values for `security_type`
        """
        return await self._get_values("securityType")

    async def get_security_types_2(self) -> list[str]:
        """
        Get the list of possible values for `security_type_2`.

        Returns:
            The list of possible values for `security_type_2`
        """
        return await self._get_values("securityType2")

    async def get_state_codes(self) -> list[str]:
        """
        Get the list of possible values for `state_code`.

        Returns:
            The list of possible values for `state_code`
        """
        return await self._get_values("stateCode")

    async def _get_values(self, key: Key) -> list[str]:
        """
        Get the current list of values for the enum-like properties on Mapping Jobs.

        Returns:
            The list of possible values for the requested field
        """
        url = self.url(f"mapping/values/{key}")
        result = await self._request(method="GET", url=url, headers=self.headers)
        values = self._json_decoder.decode(result.content)["values"]
        return cast("list[str]", values)

    async def filter(self, query: Filter, timeout: int | None = 60) -> list[FigiResult]:
        """
        Search for FIGIs using keywords and other filters.

        The results are listed alphabetically by FIGI and include the total number of results.

        Args:
            query: Query object
            timeout: The maximum time in seconds to wait for the results to be fetched

        Returns:
            list: a list of FigiResult objects
        """
        start = time.time()

        # Requests rate limitation for Search/Filter API
        # We add half a second extra
        delay = 60 / self.max_search_requests + 0.5

        url = self.url("filter")
        headers = self.headers
        data = self._json_encoder.encode(query)
        result = self._json_decoder.decode(
            (
                await self._request(
                    method="POST",
                    url=url,
                    data=data,
                    headers=headers,
                    timeout=timeout,
                )
            ).content,
        )

        mapping_job_results = self._process_filter_result(result)

        while "next" in result:
            await asyncio.sleep(delay)
            query.start = result["next"]
            data = self._json_encoder.encode(query)
            result = self._json_decoder.decode(
                (
                    await self._request(
                        method="POST",
                        url=url,
                        data=data,
                        headers=headers,
                        timeout=timeout,
                    )
                ).content,
            )
            mapping_job_results += self._process_filter_result(result)
            if timeout is not None and time.time() - start > timeout:
                logger.warning(
                    "Call timed out. Latest `next` value: %s",
                    result["next"],
                )
                break

        return mapping_job_results

    async def get_total_number_of_matches(self, query: Filter) -> int:
        """
        Return the total number of matches for a given query.

        The function only makes one call to the `filter` endpoint and returns the `total` field
        from the response.

        Args:
            query: Filter object

        Returns:
            The total number of matches as a positive integer
        """
        result = self._json_decoder.decode(
            (
                await self._request(
                    method="POST",
                    url=self.url("filter"),
                    data=self._json_encoder.encode(query),
                    headers=self.headers,
                )
            ).content,
        )
        return cast("int", result["total"])

    @staticmethod
    async def _request(
        method: str,
        url: str,
        headers: dict[str, str],
        data: bytes | None = None,
        timeout: int | None = None,
    ) -> httpx.Response:
        """
        Make remote call.

        Raises:
            HTTPError: A custom exception in case of HTTP error.
        """
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                content=data,
                timeout=timeout,
            )

        if response.status_code != httpx.codes.OK:
            raise HTTPError(response.status_code, response.text)

        return response
