from flask import render_template, request, redirect, url_for, make_response, session
from base import app
from base.com.dao.login_dao import LoginDao
from base.com.service.login_service import LoginService
from base.custom_enum.static_variables import StaticVariables
from base.utils import my_logger

logger = my_logger.get_logger()
static_variables = StaticVariables()
TOKEN = 'no-store, no-cache, must-revalidate, max-age=0'


@app.route('/')
def load_login_page():
    """Render the login page and prevent caching."""
    response = make_response(render_template('login_and_register/login.html'))
    response.headers['Cache-Control'] = TOKEN
    return response


@app.route('/home', methods=['POST', 'GET'])
def load_home_page():
    """Handle login form submission and redirect to appropriate home page."""
    if request.method == 'POST':
        try:
            username = request.form.get('register_username').strip() or None
            password = request.form.get('register_password').strip() or None

            validate_user = LoginDao.validate_login(username, password)

            if validate_user:
                user_data = validate_user.as_dict()
                if user_data['login_role'] not in ['ADMIN', 'USER']:
                    raise ValueError("Invalid user role")

                access_token, refresh_token = LoginService.generate_token(
                    user_data['login_id'],
                    user_data['login_username'],
                    user_data['login_role'])

                target_page = 'admin_home_page' if user_data[
                                                       'login_role'] == 'ADMIN' else 'user_home_page'
                response = redirect(url_for(target_page))
                response.set_cookie(static_variables.TOKEN_ACCESS_KEY,
                                    access_token,
                                    max_age=int(
                                        static_variables.ACCESS_TOKEN_EXPIRE_MINUTES) * 60,
                                    httponly=True)
                response.set_cookie(static_variables.TOKEN_REFRESH_KEY,
                                    refresh_token,
                                    max_age=int(
                                        static_variables.REFRESH_TOKEN_EXPIRE_MINUTES) * 60,
                                    httponly=True)
                logger.info(
                    f"Access & Refresh token created for user: {username}")
                return response
            else:
                raise ValueError("Invalid username or password.")

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return make_response(
                render_template("login_and_register/login.html",
                                error="Invalid username, password, or user role."))
    return redirect(url_for('load_login_page'))


@app.route('/admin/home', methods=['GET'])
@LoginService.login_required(role=static_variables.ADMIN_ROLE)
def admin_home_page():
    """Render admin home page for authenticated admin users."""
    logger.info("Admin accessing home page")
    response = make_response(render_template('home.html', no_back=True))
    response.headers['Cache-Control'] = TOKEN  # Prevent caching of the home page
    return response


@app.route('/user/home', methods=['GET'])
@LoginService.login_required(role=static_variables.USER_ROLE)
def user_home_page():
    """Render user home page for authenticated regular users."""
    logger.info("User accessing home page")
    response = make_response(render_template('user_home_page.html', no_back=True))
    response.headers['Cache-Control'] = TOKEN
    return response


@app.route('/logout')
@LoginService.login_required(role=static_variables.ADMIN_ROLE)
def logout():
    """Handle user logout."""
    session.clear()
    response = redirect(url_for('load_login_page'))

    # Delete cookies for access and refresh tokens
    response.delete_cookie(static_variables.TOKEN_ACCESS_KEY)
    response.delete_cookie(static_variables.TOKEN_REFRESH_KEY)

    logger.info("User logged out successfully")

    # Set cache control headers to prevent caching
    response.headers[
        'Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    return response

    # """Handle user logout."""
    # session.clear()
    # response = redirect(url_for('load_login_page'))
    # response.delete_cookie(static_variables.TOKEN_ACCESS_KEY)
    # response.delete_cookie(static_variables.TOKEN_REFRESH_KEY)
    # logger.info("User logged out successfully")
    # response.headers['Cache-Control'] = TOKEN
    # return response