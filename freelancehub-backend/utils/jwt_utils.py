from flask_jwt_extended import create_access_token


def generate_token(user_doc):
    # user_doc is a dict-like document from MongoDB
    identity = str(user_doc.get('_id'))
    additional = {'role': user_doc.get('role', 'client')}
    token = create_access_token(identity=identity, additional_claims=additional)
    return token