def jwt_response_payload_handler(token, user=None, request=None):
    """Handler для добвления в токен id пользователя"""
    return {
        'token': token,
        'user_id': user.id,
    }
