from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from domain.enums import ReviewStatus

@dataclass
class Review:
    id: Optional[int]
    place_id: int
    author_id: int
    rating: int
    text: str
    status: ReviewStatus
    created_at: datetime

    moderated_by: Optional[int] = None
    moderated_at: Optional[datetime] = None
    moderation_reason: Optional[str] = None

    def approve(self, moderator_id: int):
        self.status = ReviewStatus.APPROVED
        self.moderated_by = moderator_id
        self.moderated_at = datetime.utcnow()
        self.moderation_reason = None

    def reject(self, moderator_id: int, reason: str):
        self.status = ReviewStatus.REJECTED
        self.moderated_by = moderator_id
        self.moderated_at = datetime.utcnow()
        self.moderation_reason = reason
