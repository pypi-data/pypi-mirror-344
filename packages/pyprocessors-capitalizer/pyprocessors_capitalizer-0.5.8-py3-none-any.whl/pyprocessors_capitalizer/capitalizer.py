import logging
from typing import Type, List

from pydantic import BaseModel
from pymultirole_plugins.v1.processor import ProcessorParameters, ProcessorBase
from pymultirole_plugins.v1.schema import Document, Annotation

logger = logging.getLogger(__name__)


class CapitalizerParameters(ProcessorParameters):
    pass


class CapitalizerProcessor(ProcessorBase):
    __doc__ = """Capitalizer processor."""

    def process(
            self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:

        for document in documents:
            if document.annotations:
                text = document.text
                sorted_annotations = sorted([a for a in document.annotations if not a.labelName == 'sentence'],
                                            key=natural_order,
                                            reverse=True,
                                            )
                res = []
                i = 0
                for a in sorted_annotations:
                    atext = a.text or text[a.start:a.end]
                    caps = [word.capitalize() for word in atext.split()]
                    res.append(text[i:a.start] + ' '.join(caps))
                    i = a.end
                res.append(text[a.end:])
                document.text = ''.join(res)
                document.annotations = None
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return CapitalizerParameters


def left_longest_match(a: Annotation):
    return a.end - a.start, -a.start


def natural_order(a: Annotation):
    return -a.start, a.end - a.start
