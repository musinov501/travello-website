from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers


class TranslatedFieldsWriteMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.languages = settings.LANGUAGES

        translatable_fields = getattr(self, "translatable_fields", [])
        media_fields = getattr(self, "media_fields", [])

        for field_name in translatable_fields:
            is_media = field_name in media_fields

            # Base field is optional
            if field_name in self.fields:
                self.fields[field_name].required = False

            # Create language-specific fields
            for lang_code, lang_name in self.languages:
                field_key = f"{field_name}_{lang_code.lower()}"

                if is_media:
                    self.fields[field_key] = serializers.ListField(
                        child=serializers.FileField(),
                        required=False,
                        allow_empty=True,
                        help_text=f"{lang_name} files",
                    )
                elif field_name in self.fields:
                    original = self.fields[field_name]
                    self.fields[field_key] = original.__class__(
                        required=False,
                        allow_blank=True,
                        allow_null=True,
                        help_text=f"{lang_name} translation",
                        max_length=getattr(original, "max_length", None),
                    )

    def create(self, validated_data):
        media_data = self._extract_media_data(validated_data)
        instance = super().create(validated_data)
        self._save_media_files(instance, media_data)
        return instance

    def update(self, instance, validated_data):
        media_data = self._extract_media_data(validated_data)
        instance = super().update(instance, validated_data)
        self._save_media_files(instance, media_data)
        return instance

    def _extract_media_data(self, validated_data):
        """Pop out all media-related data."""
        media_fields = getattr(self, "media_fields", [])
        translatable_fields = getattr(self, "translatable_fields", [])
        media_data = {}

        for field_name in media_fields:
            is_translatable = field_name in translatable_fields

            if is_translatable:
                for lang_code, _ in self.languages:
                    key = f"{field_name}_{lang_code.lower()}"
                    if key in validated_data:
                        media_data[key] = validated_data.pop(key)
            elif field_name in validated_data:
                media_data[field_name] = validated_data.pop(field_name)

        return media_data

    def _save_media_files(self, instance, media_data):
        """Save uploaded media files."""
        from apps.shared.models import Media

        if not media_data:
            return

        content_type = ContentType.objects.get_for_model(instance)
        request = self.context.get("request")
        user = getattr(request, "user", None) if request else None

        for field_name, files in media_data.items():
            if not files:
                continue

            language = None
            for lang_code, _ in self.languages:
                suffix = f"_{lang_code.lower()}"
                if field_name.endswith(suffix):
                    language = lang_code
                    break

            file_list = files if isinstance(files, list) else [files]
            for file_obj in file_list:
                if file_obj:
                    Media.objects.create(
                        content_type=content_type,
                        object_id=instance.pk,
                        file=file_obj,
                        media_type="image",
                        original_filename=getattr(file_obj, "name", None),
                        uploaded_by=user,
                        language=language,
                        is_public=True,
                    )


class TranslatedFieldsReadMixin:
    """Handle representation for web vs mobile devices with fallbacks."""

    def to_representation(self, instance):
        data = super().to_representation(instance)

        translatable_fields = getattr(self, "translatable_fields", [])
        media_fields = getattr(self, "media_fields", [])
        request = self.context.get("request")

        device_type = getattr(request, "device_type", "WEB") 
        lang = getattr(request, "lang", None)

        for field_name in translatable_fields:
            is_media = field_name in media_fields

            if is_media:
                # Media handling
                if device_type == "MOBILE" and lang:
                    data[field_name] = self._get_media(instance, field_name, lang)
                else:
                    # web → return all media
                    all_media = []
                    for lc, _ in settings.LANGUAGES:
                        all_media.extend(self._get_media(instance, field_name, lc.lower()))
                    data[field_name] = all_media
            else:
                # Text fields handling
                if device_type == "MOBILE" and lang:
                    # Prefer language-specific attribute, fall back to base field
                    value = None
                    # try model attribute first
                    value = getattr(instance, f"{field_name}_{lang}", None)
                    if value in (None, ""):
                        value = getattr(instance, field_name, "")
                    data[field_name] = value or ""
                    # remove any _en/_uz etc fields if present
                    for lc, _ in settings.LANGUAGES:
                        key = f"{field_name}_{lc.lower()}"
                        data.pop(key, None)
                else:
                    # Web → show all languages; if per-lang attr missing, show base field as fallback
                    for lc, _ in settings.LANGUAGES:
                        per_attr = getattr(instance, f"{field_name}_{lc.lower()}", None)
                        if per_attr in (None, ""):
                            per_attr = getattr(instance, field_name, "")
                        data[f"{field_name}_{lc.lower()}"] = per_attr or ""
                    data.pop(field_name, None)

        return data

    def _get_media(self, instance, field_name, language):
        """Return list of media dicts filtered by language.

        Supports:
         - model related manager `media_files` (preferred),
         - a FileField/ImageField on the instance (e.g., instance.image),
         - serialized dicts (instance may be a dict).
        """
        # 1) If instance has a related manager media_files, use it
        qs_or_list = []

        if hasattr(instance, "media_files") and hasattr(getattr(instance, "media_files"), "filter"):
            try:
                qs_or_list = instance.media_files.filter(language__iexact=language)
            except Exception:
                qs_or_list = []
        else:
            # 2) If instance is a dict (serialized) and contains media under common keys
            if isinstance(instance, dict):
                candidate = instance.get("media_files") or instance.get(field_name) or []
                # candidate might be a list of dicts
                qs_or_list = candidate
            else:
                # 3) If the model has a FileField/ImageField named field_name, return it (single file)
                file_attr = getattr(instance, field_name, None)
                if file_attr:
                    # file_attr might be a FieldFile object; return it as a single-item list
                    qs_or_list = [file_attr]

        result = []
        for m in qs_or_list:
            if isinstance(m, dict):
                file_url = m.get("file") or m.get("url") or None
                filename = m.get("original_filename") or m.get("filename") or None
                lang = m.get("language")
                id_ = str(m.get("id")) if m.get("id") else None
                result.append({"id": id_, "url": file_url, "filename": filename, "language": lang})
            else:
                # m might be a FieldFile or a model instance of Media
                # If it's a FieldFile (has url), map it
                url = getattr(getattr(m, "file", m), "url", None)
                filename = getattr(m, "original_filename", None) or getattr(m, "name", None)
                lang = getattr(m, "language", None)
                id_ = str(getattr(m, "id", None)) if getattr(m, "id", None) is not None else None
                result.append({"id": id_, "url": url, "filename": filename, "language": lang})
        return result