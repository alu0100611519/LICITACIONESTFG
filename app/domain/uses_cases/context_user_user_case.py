

class ContextUserUseCase:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def get_user_context(self, user_id):
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return {
            "user_id": user.id,
            "user_name": user.name,
            "user_email": user.email,
            "user_role": user.role,
        }