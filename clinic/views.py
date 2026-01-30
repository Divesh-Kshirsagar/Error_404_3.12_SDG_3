from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Max

from .models import Patient, Case
from .services import analyze_symptoms


class IntakeView(View):
    """Handle patient intake with voice transcript submission."""
    
    template_name = 'clinic/intake.html'
    
    def get(self, request):
        """Render the intake form."""
        return render(request, self.template_name)
    
    def post(self, request):
        """Process the intake form submission."""
        # Check for fallback manual entry
        name = request.POST.get('name', '').strip()
        age = request.POST.get('age', '').strip()
        phone = request.POST.get('phone', '').strip()
        transcript = request.POST.get('transcript', '').strip()
        
        # If no transcript and no manual data, error
        if not transcript and not (name and age):
            return render(request, self.template_name, {
                'error': 'Please describe your symptoms or fill in the form manually.'
            })
            
        # Analyze symptoms & extract details
        analysis = analyze_symptoms(transcript)
        
        # Use extracted details if manual not provided
        final_name = name if name else analysis.get('name')
        final_age = age if age else analysis.get('age')
        
        # If extraction failed and no manual input, ask for manual input
        if not final_name or not final_age:
            # Render form again with extraction failure message and fill what we have
            return render(request, self.template_name, {
                'error': 'Could not catch your name or age. Please enter them manually.',
                'transcript': transcript, # Keep the transcript so they don't have to speak again
                'show_manual': True
            })
            
        # Get or create patient
        # Note: In a real app we'd match better than just name/phone
        patient, _ = Patient.objects.get_or_create(
            name=final_name,
            defaults={'age': final_age, 'phone': phone}
        )
        
        # Determine Doctor Assignment based on Risk
        # > 0.7 Risk -> Senior Doctor
        if analysis['risk_score'] > 0.7:
            assigned_doctor = "Dr. Senior (Emergency)"
        else:
            assigned_doctor = "Dr. Junior (General)"
            
        # Generate Token Number (Simple Auto-Increment Logic for MVP)
        last_token = Case.objects.aggregate(Max('token_number'))['token_number__max']
        new_token = (last_token or 0) + 1
        
        # Create the case
        case = Case.objects.create(
            patient=patient,
            transcript=transcript,
            symptoms=analysis['symptoms'],
            risk_score=analysis['risk_score'],
            status='waiting',
            token_number=new_token,
            assigned_doctor=assigned_doctor
        )
        
        # Redirect to Token View
        return redirect('clinic:token', case_id=case.id)


class TokenView(View):
    """Display the assigned token and wait time."""
    template_name = 'clinic/token.html'
    
    def get(self, request, case_id):
        case = get_object_or_404(Case, id=case_id)
        
        # Simple wait time estimation: 10 mins per waiting patient ahead
        waiting_ahead = Case.objects.filter(
            status='waiting', 
            created_at__lt=case.created_at,
            risk_score__lte=case.risk_score if case.risk_score <= 0.7 else 1.0 # Simple bucket logic
        ).count()
        
        est_wait_time = (waiting_ahead + 1) * 10 
        
        return render(request, self.template_name, {
            'case': case,
            'est_wait_time': est_wait_time
        })


class DashboardView(View):
    """Display the doctor's dashboard with split queue view and active patient."""
    
    template_name = 'clinic/dashboard.html'
    
    def get(self, request):
        return self._render_dashboard(request)
    
    def post(self, request):
        """Handle case actions: Next Patient, Update Medical Record."""
        action = request.POST.get('action')
        case_id = request.POST.get('case_id')
        
        if action == 'next_patient':
            # 1. Mark current active case as completed (if exists)
            Case.objects.filter(is_active=True).update(status='completed', is_active=False)
            
            # 2. Pick next best patient (Highest Risk -> Oldest Time)
            next_case = Case.objects.filter(status='waiting').order_by('-risk_score', 'created_at').first()
            if next_case:
                next_case.is_active = True
                next_case.save()
                
        elif action == 'save_record':
            # Save notes for the active case
            if case_id:
                case = Case.objects.get(id=case_id)
                case.prescription = request.POST.get('prescription', '')
                case.diagnosis = request.POST.get('diagnosis', '')
                case.save()
        
        elif action == 'complete_current':
             # Mark active as completed
             if case_id:
                case = Case.objects.get(id=case_id)
                case.status = 'completed'
                case.is_active = False
                case.save()

        
        # HTMX partial update
        if request.headers.get('HX-Request'):
             return self._render_dashboard(request, partial=True)
             
        return redirect('clinic:dashboard')

    def _render_dashboard(self, request, partial=False):
        # Get Active Case
        active_case = Case.objects.filter(is_active=True).first()
        
        # Get Waiting Queues
        waiting_cases = Case.objects.filter(status='waiting', is_active=False)
        junior_queue = waiting_cases.filter(risk_score__lte=0.7).order_by('-risk_score', 'created_at')
        senior_queue = waiting_cases.filter(risk_score__gt=0.7).order_by('-risk_score', 'created_at')
        
        # Get History for Active Patient
        patient_history = []
        if active_case:
            patient_history = Case.objects.filter(
                patient=active_case.patient, 
                status='completed'
            ).order_by('-created_at')
            
        context = {
            'active_case': active_case,
            'patient_history': patient_history,
            'junior_queue': junior_queue,
            'senior_queue': senior_queue,
            'total_waiting': waiting_cases.count(),
        }
        
        if partial:
             # Return just the content part for HTMX
             return render(request, 'clinic/partials/dashboard_content.html', context)
             
        return render(request, self.template_name, context)


class QueuePartialView(View):
    """HTMX endpoint for polling queue updates."""
    
    def get(self, request):
        """Return updated queue tables."""
        # Simple reuse of dashboard render for now, or just the queue table
        # For simplicity, we'll re-render the whole dashboard content partial as the queue affects active state
        dashboard_view = DashboardView()
        return dashboard_view._render_dashboard(request, partial=True)
