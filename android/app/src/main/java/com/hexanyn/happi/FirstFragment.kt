package com.hexanyn.happi

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.RelativeLayout
import android.widget.TextView
import androidx.navigation.fragment.findNavController
import com.android.volley.Request
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.Volley

/**
 * A simple [Fragment] subclass as the default destination in the navigation.
 */
class FirstFragment : Fragment() {

    override fun onCreateView(
            inflater: LayoutInflater, container: ViewGroup?,
            savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_first, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        view.findViewById<Button>(R.id.button_login).setOnClickListener {
            findNavController().navigate(R.id.action_FirstFragment_to_SecondFragment)
        }

        view.findViewById<Button>(R.id.button_first).setOnClickListener {
            findNavController().navigate(R.id.action_FirstFragment_to_SecondFragment)
        }

        val textView = view.findViewById<TextView>(R.id.textview)

        val queue = Volley.newRequestQueue(context)
        val url = "https://happi.hexanyn.fr/api/me/"

        val stringRequest = object: JsonObjectRequest(Request.Method.GET, url, null,
                { response ->
                    val data = response.getJSONArray("results").getJSONObject(0)
                    val count = data.getJSONObject("count")
                    textView.text = "Welcome ${data["username"]}\n" +
                            "${count["slots"]} slot(s)\n" +
                            "${count["invites"]} invite(s)\n" +
                            "${count["accepted"]} accepted invite(s)"
                    showPanel(view)
                },
                { error ->
                    textView.text = "That didn't work: ${error.toString()}"
                    showPanel(view)
                })
        {
            override fun getHeaders(): MutableMap<String, String> {
                val headers = HashMap<String, String>()
				token = ""
                headers["Authorization"] = "Token $token"
                return headers
            }
        }

        queue.add(stringRequest)

    }

    fun showPanel(view: View) {
        view.findViewById<RelativeLayout>(R.id.viewPanel).visibility = View.VISIBLE
        view.findViewById<RelativeLayout>(R.id.loadingPanel).visibility = View.INVISIBLE
    }
}
