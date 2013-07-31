from models import NoahUser
import noah.utils as util
import logging
logger = logging.getLogger(__name__)

class NEWTBackend:
    """
    Authenticate against NEWT.

    """

    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False

    def authenticate(self, username=None, password=None):
        url="/auth"
        params={'username': username, 'password': password}

        response, content = util.newt_request(url, 'POST', params=params)

        # If the user was logged in:
        if response.json()['auth']:
            
            try:
                user = NoahUser.objects.get(username=username)
                logger.debug("Existing user logged in: %s" % username)
                user.set_cookie(cookie_str=response.headers['set-cookie'])
            except NoahUser.DoesNotExist:
                logger.debug("New user: %s" % username)
                # Create a new user.
                try:
                    user = NoahUser(username=username)
                    # TODO: remove once other interfaces are ready
                    user.set_cookie(cookie_str=response.headers['set-cookie'])
                except Exception, e:
                    logger.warning('User creation failed: %s' % str(e))
              
            # TODO: Set the cookie somewhere?
            return user
        
        logger.debug("Auth failed")
        return None

    def get_user(self, user_id):
        try:
            return NoahUser.objects.get(pk=user_id)
        except NoahUser.DoesNotExist:
            return None
