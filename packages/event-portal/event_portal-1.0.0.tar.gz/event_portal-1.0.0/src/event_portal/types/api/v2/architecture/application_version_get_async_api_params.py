# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Annotated, TypedDict

from ....._utils import PropertyInfo

__all__ = ["ApplicationVersionGetAsyncAPIParams"]


class ApplicationVersionGetAsyncAPIParams(TypedDict, total=False):
    async_api_version: Annotated[Literal["2.0.0", "2.2.0", "2.5.0"], PropertyInfo(alias="asyncApiVersion")]
    """The version of AsyncAPI to use."""

    context_id: Annotated[str, PropertyInfo(alias="contextId")]
    """
    Applies bindings from subscribed events that are published in this event broker
    or event mesh.
    """

    context_type: Annotated[Literal["eventBroker", "eventMesh"], PropertyInfo(alias="contextType")]
    """The context of which events are attracted from."""

    environment_options: Annotated[
        Literal["include_declared_and_attracted_events", "include_attracted_events_only"],
        PropertyInfo(alias="environmentOptions"),
    ]
    """
    Determines whether bindings are applied to declared subscribed events or
    published subscribed events in the event mesh or both.

    Replacement: Use expand instead.

    Reason: The change is to allow for increased flexibility of the API.

    Removal Date: 2025-09-20 18:00:00.000.
    """

    expand: Literal[
        "declaredSubscribedEvents",
        "attractedEvents",
        "servers",
        "serverBindings",
        "declaredSubscribedEventBindings",
        "attractedEventBindings",
    ]
    """A comma separated list of sections of the asyncapi document to include."""

    format: Literal["json", "yaml"]
    """The format in which to get the AsyncAPI specification.

    Possible values are yaml and json.
    """

    included_extensions: Annotated[
        Literal["all", "parent", "version", "none"], PropertyInfo(alias="includedExtensions")
    ]
    """The event portal database keys to include for each AsyncAPI object."""

    messaging_service_id: Annotated[str, PropertyInfo(alias="messagingServiceId")]
    """
    Applies bindings from attracted events that are published in this messaging
    service's modeled event mesh.

    Replacement: Use contextId with contextType instead.

    Reason: The change is to allow for increased flexibility of the API.

    Removal Date: 2025-09-20 18:00:00.000.
    """

    show_versioning: Annotated[bool, PropertyInfo(alias="showVersioning")]
    """
    Include versions in each AsyncAPI object's name when only one version is present
    """
