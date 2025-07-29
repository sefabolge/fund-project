from rest_framework import generics
from ..models import Fund
from .serializer import FundSerializer
import logging

logger = logging.getLogger("funds")

class FundListAPI(generics.ListAPIView):
    serializer_class = FundSerializer

    def get_queryset(self):
        strategy = self.request.query_params.get("strategy")
        if strategy:
            logger.info(f"Filtering funds by strategy: {strategy}")
            return Fund.objects.filter(strategy=strategy)
        logger.info("Returning all funds via API")
        return Fund.objects.all()

class FundDetailAPI(generics.RetrieveAPIView):
    queryset = Fund.objects.all()
    serializer_class = FundSerializer
