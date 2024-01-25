from rest_framework.views import APIView
from rest_framework.response import Response

from .utls import generate_verification_code, send_verification_code


class SendVerificationCode(APIView):
    def post(self, request):
        email = request.data.get('email')

        if email:
            verification_code = generate_verification_code()
            send_verification_code(email, verification_code)
            return Response({'message': 'Verification code sent successfully.'})
        else:
            return Response({'error': 'Email not provided.'}, status=400)
