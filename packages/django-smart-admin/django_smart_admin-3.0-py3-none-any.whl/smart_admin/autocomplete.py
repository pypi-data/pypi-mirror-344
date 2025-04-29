from django.apps import apps
from django.contrib.admin.views.autocomplete import AutocompleteJsonView
from django.core.exceptions import FieldDoesNotExist, PermissionDenied
from django.http import Http404


class SmartAutocompleteJsonView(AutocompleteJsonView):
    """Handle AutocompleteWidget's AJAX requests for data."""

    paginate_by = 20
    admin_site = None

    def serialize_result(self, obj, to_field_name):
        self._labelize = str
        if hasattr(self.model_admin, "get_autocomplete_label"):
            return self.model_admin.get_autocomplete_label
        return {"id": str(getattr(obj, to_field_name)), "text": self._labelize(obj)}

    def get_queryset(self):
        """Overriden to work also with fields without `choices` attribute."""
        qs = self.model_admin.get_queryset(self.request)
        if hasattr(self.source_field, "get_limit_choices_to"):
            qs = qs.complex_filter(self.source_field.get_limit_choices_to())
        qs, search_use_distinct = self.model_admin.get_search_results(self.request, qs, self.term)
        if search_use_distinct:
            qs = qs.distinct()
        return qs

    def process_request(self, request):  # noqa C901
        """
        Validate request integrity, extract and return request parameters.

        Since the subsequent view permission check requires the target model
        admin, which is determined here, raise PermissionDenied if the
        requested app, model or field are malformed.

        Raise Http404 if the target model admin is not configured properly with
        search_fields.
        """
        term = request.GET.get("term", "")
        try:
            app_label = request.GET["app_label"]
            model_name = request.GET["model_name"]
            field_name = request.GET["field_name"]
        except KeyError as e:
            raise PermissionDenied from e

        # Retrieve objects from parameters.
        try:
            source_model = apps.get_model(app_label, model_name)
        except LookupError as e:
            raise PermissionDenied from e

        try:
            source_field = source_model._meta.get_field(field_name)
        except FieldDoesNotExist as e:
            raise PermissionDenied from e
        if source_field.remote_field:
            try:
                remote_model = source_field.remote_field.model
            except AttributeError as e:
                raise PermissionDenied from e
        else:
            try:
                remote_model = source_field.model
            except AttributeError as e:
                raise PermissionDenied from e

        try:
            model_admin = self.admin_site._registry[remote_model]
        except KeyError as e:
            raise PermissionDenied from e

        # Validate suitability of objects.
        if not model_admin.get_search_fields(request):
            raise Http404("%s must have search_fields for the autocomplete_view." % type(model_admin).__qualname__)

        to_field_name = getattr(source_field.remote_field, "field_name", remote_model._meta.pk.attname)
        to_field_name = remote_model._meta.get_field(to_field_name).attname
        if not model_admin.to_field_allowed(request, to_field_name):
            raise PermissionDenied

        return term, model_admin, source_field, to_field_name

    def has_perm(self, request, obj=None):
        """Check if user has permission to access the related model."""
        return self.model_admin.has_view_permission(request, obj=obj)
