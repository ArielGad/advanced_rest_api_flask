## Advanced Rest API Flask

Note - this repo is based and extends rest_api_flask repo

######Packages in use:
- Type hints (complex)
- Marshmallow
- Mailgun (site)


######Remember:
- 
@app.errorhandler(ValidationError)

Deleted decorators:
 - @jwt.user_claims_loader
 - @jwt.token_in_blacklist_loader
 - @jwt.expired_token_loader
 - @jwt.invalid_token_loader
 - @jwt.unauthorized_loader
 - @jwt.needs_fresh_token_loader
 - @jwt.revoked_token_loader
