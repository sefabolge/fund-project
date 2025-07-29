from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.timezone import now
from django.core.files.storage import default_storage
from .forms import FundUploadForm
from .services.fund_importer import import_funds_from_csv
import io
from django.views.generic import ListView
from django.db.models import Sum
from .models import Fund

from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
import logging

logger = logging.getLogger("funds")


# Handles GET and POST requests for uploading fund CSVs.
# - GET: renders the upload form.
# - POST: processes and imports the uploaded CSV file.
class FundUploadView(View):
    template_name = "funds/fund_upload.html"

    def get(self, request):
        return render(request, self.template_name, {"form": FundUploadForm()})

    def post(self, request):
        form = FundUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save uploaded file with timestamped filename
            csv_file = form.cleaned_data["csv_file"]
            filename = csv_file.name
            path = f"fund_uploads/{now().strftime('%Y%m%d_%H%M%S')}_{filename}"
            saved_path = default_storage.save(path, csv_file)

            try:
                # Convert to text stream and import
                with default_storage.open(saved_path, "rb") as f:
                    text_stream = io.TextIOWrapper(f, encoding="utf-8-sig")
                    created, updated = import_funds_from_csv(text_stream)

                msg = f"Import complete: {created} created, {updated} updated."
                messages.success(request, msg)
                logger.info(msg)

            except Exception as e:
                logger.exception("CSV import failed.")
                messages.error(request, f"Import failed: {str(e)}")

            return redirect("funds:fund_list")

        return render(request, self.template_name, {"form": form})
    
# Displays a list of all funds with optional filtering by strategy
class FundListView(ListView):
    model = Fund
    template_name = "funds/fund_list.html"
    context_object_name = "funds"
    paginate_by = 25  # Optional: Add pagination if needed

    def get_queryset(self):
        queryset = super().get_queryset()
        self.selected_strategy = self.request.GET.get("strategy")
        if self.selected_strategy:
            queryset = queryset.filter(strategy=self.selected_strategy)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filtered_funds = context["funds"]

        # Normalize and deduplicate strategies
        raw_strategies = Fund.objects.values_list("strategy", flat=True)
        cleaned_strategies = sorted(set(
            s.strip().title() for s in raw_strategies if s and s.strip()
        ))

        context.update({
            "strategies": cleaned_strategies,
            "selected_strategy": self.selected_strategy,
            "total_count": filtered_funds.count(),
            "total_aum": filtered_funds.aggregate(Sum("aum"))["aum__sum"] or 0,
        })
        return context
    
# Clears all fund records from the database (This part optional to test quickly, can handle in admin)
@method_decorator(require_POST, name="dispatch")
class ClearAllFundsView(View):
    def post(self, request):
        Fund.objects.all().delete()
        messages.success(request, "All funds deleted.")
        return redirect("funds:fund_list")