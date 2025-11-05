import asyncio
from typing import List, Dict
from app.recs.recs_loader import recs_html_generator
from app.recs.recs_parser import generate_paragraphs_from_html
from app.recs.dao import ParagraphDAO


class RecsService:
    def __init__(self):
        self._is_loading = False

    async def reload_recs(self):
        """Reload recommendations in background"""
        if self._is_loading:
            return {"status": "already_loading"}

        self._is_loading = True
        try:
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            html_list = await loop.run_in_executor(
                None,  # Use default thread pool
                lambda: list(recs_html_generator(update_report=False))
            )

            paragraphs = []
            for html in html_list:
                try:
                    pg_gen = generate_paragraphs_from_html(html)
                    for pg in pg_gen:
                        await ParagraphDAO.add(**pg._asdict())
                except Exception as e:
                    print(f'Failed to parse HTML: {e}')

            self._paragraphs = paragraphs
            return {"status": "success"}

        except Exception as e:
            print(f'Failed to reload recommendations: {e}')
            return {"status": "error"}
        finally:
            self._is_loading = False

    def get_paragraphs(self) -> List[Dict]:
        return self._paragraphs

    def is_loading(self) -> bool:
        return self._is_loading


# Global instance
recs_service = RecsService()
