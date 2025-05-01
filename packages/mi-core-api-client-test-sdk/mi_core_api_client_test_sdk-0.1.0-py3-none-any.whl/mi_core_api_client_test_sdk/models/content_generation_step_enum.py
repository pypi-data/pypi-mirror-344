from enum import Enum


class ContentGenerationStepEnum(str, Enum):
    CHANNEL_CONTENT_RESTRICTIONS = "channel_content_restrictions"
    CHANNEL_CONTENT_SEED_KEYWORDS = "channel_content_seed_keywords"
    CHANNEL_STORYBOARD = "channel_storyboard"
    COLLECT_SERP_DATA = "collect_serp_data"
    COLLECT_YOUTUBE_CHANNELS = "collect_youtube_channels"
    COLLECT_YOUTUBE_VIDEOS = "collect_youtube_videos"
    RELATED_TOPICS = "related_topics"
    YOUTUBE_CHANNELS_CONTENT_SUMMARY = "youtube_channels_content_summary"
    YOUTUBE_CHANNELS_COVERAGE = "youtube_channels_coverage"

    def __str__(self) -> str:
        return str(self.value)
