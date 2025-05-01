from enum import Enum


class PromptType(str, Enum):
    EMAIL_GENERATION = "email_generation"
    GENERATE_CHANNEL_CONTENT_SUMMARY_TEMPLATE = "generate_channel_content_summary_template"
    GENERATE_RELATED_KEYWORDS = "generate_related_keywords"
    GENERATE_RESTRICTIONS = "generate_restrictions"
    GENERATE_SEED_KEYWORDS = "generate_seed_keywords"
    SCENE_IMG_GENERATION = "scene_img_generation"
    SCENE_IMG_GENERATION_STYLE = "scene_img_generation_style"
    STORYBOARD_GENERATION = "storyboard_generation"
    STORYBOARD_THUMBNAIL_GENERATION = "storyboard_thumbnail_generation"
    VIDEO_ANALYZE_TEMPLATE = "video_analyze_template"

    def __str__(self) -> str:
        return str(self.value)
