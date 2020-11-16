package com.hexanyn.happi.data

import android.widget.TextView
import android.widget.Toast
import com.android.volley.Request
import com.android.volley.RequestQueue
import com.android.volley.toolbox.*
import com.hexanyn.happi.R
import com.hexanyn.happi.data.model.LoggedInUser
import com.hexanyn.happi.ui.login.LoginActivity
import org.json.JSONObject
import java.io.IOException
import java.lang.Thread.sleep
import java.util.concurrent.TimeUnit


/**
 * Class that handles authentication w/ login credentials and retrieves user information.
 */
class LoginDataSource {

    fun login(username: String, password: String): Result<LoggedInUser> {
        try {
            // TODO: handle loggedInUser authentication
            // Instantiate the cache
            val cacheDir = createTempFile("toto")
            val cache = DiskBasedCache(cacheDir, 1024 * 1024) // 1MB cap

            // Set up the network to use HttpURLConnection as the HTTP client.
            val network = BasicNetwork(HurlStack())

            // Instantiate the RequestQueue with the cache and network. Start the queue.
            val queue = RequestQueue(cache, network).apply {
                start()
            }
            val future = RequestFuture.newFuture<JSONObject>()
            val url = "https://happi.hexanyn.fr/api-token-auth/"
            val params = HashMap<String, String>()
            params["username"] = username
            params["password"] = password
            val data = JSONObject(params as Map<*, *>)
            val request = JsonObjectRequest(Request.Method.POST, url, data, future, future)
            queue.add(request)
            val response: JSONObject = future.get(5, TimeUnit.SECONDS)
            val user = LoggedInUser(response.getString("token"))
            return Result.Success(user)
        } catch (e: Throwable) {
            return Result.Error(IOException("Error logging in", e))
        }
    }

    fun logout() {
        // TODO: revoke authentication
    }
}