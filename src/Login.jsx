import "./styles/login.scss"

export const Login = {
    setup(props) {

        window.google_login = (x) => fetch("/api/login", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ credential: x.credential })
        }).then(x => {
            location.pathname = "/"
        })

        return () => {
            return <div id="google-sso">
                <div id="g_id_onload" data-client_id="4862407941-gli3asais585k29vjbnlvnh45sanjvme.apps.googleusercontent.com"
                    data-callback="google_login" data-auto_prompt="false" data-ux_mode="popup">
                </div>
                <div class="g_id_signin" data-type="standard" data-size="large" data-theme="outline" data-text="sign_in_with"
                    data-shape="rectangular" data-logo_alignment="left">
                </div>
            </div>
        }
    }
}