using System;
using System.Net;
using System.Threading;
using System.Linq;
using System.Text;
using System.Diagnostics;
using System.Net.Sockets;

/* this si a modified code
 * the original code
 * https://www.codehosting.net/blog/BlogEngine/post/Simple-C-Web-Server.aspx
 */

namespace SimpleWebServer
{

    public class WebServer
    {
        private readonly HttpListener _listener = new HttpListener();
        private readonly Func<HttpListenerRequest, string> _responderMethod;

        public WebServer(string[] prefixes, Func<HttpListenerRequest, string> method)
        {
            if (!HttpListener.IsSupported)
                throw new NotSupportedException(
                    "Needs Windows XP SP2, Server 2003 or later.");

            // URI prefixes are required, for example 
            // "http://192.168.0.xxx:8080/index/".
            if (prefixes == null || prefixes.Length == 0)
                throw new ArgumentException("prefixes");

            // A responder method is required
            if (method == null)
                throw new ArgumentException("method");

            foreach (string s in prefixes)
                _listener.Prefixes.Add(s);

            _responderMethod = method;
            _listener.Start();
        }

        public WebServer(Func<HttpListenerRequest, string> method, params string[] prefixes)
            : this(prefixes, method) { }

        public void Run()
        {
            ThreadPool.QueueUserWorkItem((o) =>
            {
                Console.WriteLine("Webserver Avviato...");
                try
                {
                    while (_listener.IsListening)
                    {
                        ThreadPool.QueueUserWorkItem((c) =>
                        {
                            var ctx = c as HttpListenerContext;
                            try
                            {
                                string rstr = _responderMethod(ctx.Request);
                                byte[] buf = Encoding.UTF8.GetBytes(rstr);
                                ctx.Response.ContentLength64 = buf.Length;
                                ctx.Response.OutputStream.Write(buf, 0, buf.Length);
                            }
                            catch { } // suppress any exceptions
                            finally
                            {
                                // always close the stream
                                ctx.Response.OutputStream.Close();
                            }
                        }, _listener.GetContext());
                    }
                }
                catch { } // suppress any exceptions
            });
        }

        public void Stop()
        {
            _listener.Stop();
            _listener.Close();
        }
    }

    class Program
    {

         
        static void Main(string[] args)
        {

            // get ip
            Console.WriteLine(Dns.GetHostName());
            IPAddress[] localIPs = Dns.GetHostAddresses(Dns.GetHostName());
            string localIP = "?";
            IPAddress addr = localIPs[1]; // se l'indirizzo ip non viene trovato cambiare l'indice da 0 a 1,2,3....

            if (addr.AddressFamily == AddressFamily.InterNetwork)
            {
                localIP = addr.ToString();
                Console.WriteLine("Server raggiungibile a questo indirizzo http://" + localIP + ":8080/");
                Console.WriteLine("indirizzo per Volume UP http://" + localIP + ":8080/volumeup");
                Console.WriteLine("indirizzo per Volume Down http://" + localIP + ":8080/volumedown");
                Console.WriteLine("NOTA, di default viene eseguito volume up se l'indirizzo non specifica volumedown");

                Console.WriteLine("directory di lavoro " + AppDomain.CurrentDomain.BaseDirectory);
            }
            else
            { 
                Console.WriteLine ("errore non trovato indirizzo IP");
                Console.WriteLine("directory di lavoro " + AppDomain.CurrentDomain.BaseDirectory);
            }
            

            WebServer ws = new WebServer(SendResponse, "http://" + localIP +  ":8080/");
            ws.Run();
            Console.WriteLine("Un semplice webserver per gestire i picchi di volume");
            Console.ReadKey();
            ws.Stop();
        }

        public static string SendResponse(HttpListenerRequest request)
        {
            if (request.RawUrl.ToString() == "/volumedown/")
            {

                Process.Start(AppDomain.CurrentDomain.BaseDirectory + "nircmd.exe", "changesysvolume -3000");
                return string.Format("<HTML><BODY>Volume Down</BODY></HTML>");

            }
            else
            {
                Process.Start(AppDomain.CurrentDomain.BaseDirectory  + "nircmd.exe", "changesysvolume 3000");
                return string.Format("<HTML><BODY>Volume Up</BODY></HTML>");
            
            }

        }
    }
}