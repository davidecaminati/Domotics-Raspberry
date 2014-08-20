/* Programma scritto da Davide Caminati il 3/8/2014
 * davide.caminati@gmail.com
 * http://caminatidavide.it/
 * 
 * licenza copyleft 
 * http://it.wikipedia.org/wiki/Copyleft#Come_si_applica_il_copyleft
 */

// TODO 
// cleanup del codice

/* Example of c:\configfile.txt  the configuration file
@http://feeds.ilsole24ore.com/c/32276/f/438662/index.rss
@http://feeds.ilsole24ore.com/c/32276/f/566660/index.rss
|COM9
 */ 

// COMANDI
// ESC per uscire
// INVIO per leggere articolo
// slide per cambiare articolo
// button1 per cambio pagine
// button2 per pause
// button3 per play

// NOTE
// address.Text = "http://webvoice.tingwo.co/ilsole5642813vox?url=";


using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.Xml;
using System.ServiceModel.Syndication;
using System.Speech.Synthesis;
using System.IO;
using System.Text.RegularExpressions;
using System.Net;
using System.IO.Ports;
using System.Diagnostics;

namespace RSSReader
{
    public partial class Form1 : Form
    {
        // VARIABLES
        bool onPause = false; // variable for trace WindowsMediaPlayer state
        int buttonState1 = 1;
        int buttonState2 = 1;
        int buttonState3 = 1;
        string portName = "";
        List<ListViewItem> newsPage = new List<ListViewItem>();
        List<string> listUrl = new List<string>();

        string mp3PathFile = @"c:\myfile.mp3";
        string lastUrl = "";
        int actualIndex = 0;
        int slideStart = 0;
        int lastSlideValue = 0;

        bool TitoloDaLeggere = false;
        int numElementInPage = 7; // Depends on Arduino Slide Settings

        // OBJECTS
        WebBrowser Wb = new WebBrowser();
        WMPLib.WindowsMediaPlayer Player;
        SerialPort Sp ;
        SpeechSynthesizer Synth = new SpeechSynthesizer();

        public Form1()
        {
            InitializeComponent();
            //ParlaBloccante("caricamento lista articoli, attendere");
            Wb.DocumentCompleted += Wb_DocumentCompleted;

            Synth.SetOutputToDefaultAudioDevice();  // Configure the audio output for speech synth. 

            ReadConfigFile();                       // read config (urls, serial port)
            popolalistNewsComplete();               // create news from RSS Feeds into listNewsComplete

            Sp = new SerialPort(portName);
            LeggiTitoloNews();
        }

        /// <summary>
        /// lettura titolo delle news (viene lanciato automaticamente quando si seleziona una news)
        /// </summary>
        private void LeggiTitoloNews()
        {
            //stop eventualy other file
            StopFile();
            try
            {
                if (Wb.Document != null)
                {
                    Wb.Document.OpenNew(true);
                    Wb.Document.Write(newsPage[actualIndex].SubItems[1].Text);
                }
                else
                {
                    Wb.DocumentText = newsPage[actualIndex].SubItems[1].Text;
                }
                Parla(actualIndex.ToString() + ". " + newsPage[actualIndex].Text); //numero e poi titolo notizia
            }
            catch 
            {
            }
        }

        /// <summary>
        /// Carica l'elenco delle news dai feed RSS usando l'elenco degli indirizzi caricati durante la lettura del file di configurazione
        /// </summary>
        private void popolalistNewsComplete()
        {
            foreach (string u in listUrl) 
            {
                Read_RSS(u); 
            }
        }


        private void Form1_Load(object sender, EventArgs e)
        {
            Wb.ScriptErrorsSuppressed = true;
            
            if (newsPage.Count > 0)
            {
                OpenSerialPort();   // Open the serial port
            }
            else
            {
                ParlaBloccante("Errore durante caricamento lista articoli. programma bloccato, si consiglia di chiudere il programma");
            }
        }

        /// <summary>
        /// Estrae l'elenco delle news dal singolo feed RSS
        /// </summary>
        /// <param name="indirizzo">url completo del feed RSS</param>
        private void Read_RSS(string indirizzo)
        {
            try
            {
                XmlReader reader = XmlReader.Create(indirizzo);
                SyndicationFeed feed = SyndicationFeed.Load(reader);
                foreach (SyndicationItem s in feed.Items)
                {
                    string[] r = {s.Title.Text, s.Links[0].Uri.ToString() };
                    newsPage.Add(new ListViewItem(r));
                }
            }
            catch (Exception ex) 
            {
                ParlaBloccante("Errore nella lettura del feed. messaggio:" + ex.Message);
            }
        }


        private void Muto()
        {
            Synth.SpeakAsyncCancelAll();
        }

        /// <summary>
        /// attiva il Synt vocale e riproduce il testo passato come parametro (puo' essere interrotto da un'altra riproduzione)
        /// </summary>
        /// <param name="args">testo da pronunciare</param>
        private void Parla(string args)
        {
            Muto();
            Synth.SpeakAsyncCancelAll();
            Synth.SpeakAsync(args);
        }

        /// <summary>
        /// attiva il Synt vocale e riproduce il testo passato come parametro (NON puo' essere interrotto da un'altra riproduzione)
        /// </summary>
        /// <param name="args">testo da pronunciare</param>
        private void ParlaBloccante(string args)
        {
            Muto();
            Synth.SpeakAsyncCancelAll();
            Synth.Speak(args);
        }

        
        private void ReadConfigFile()
        {
            try
            {
                string line;
                // Read the configuration file line by line.
                System.IO.StreamReader file = new System.IO.StreamReader(@"c:\configfile.txt");
                while ((line = file.ReadLine()) != null)
                {
                    if (line.StartsWith("@"))
                    {
                        listUrl.Add(line.Split('@')[1]);
                    }
                    if (line.StartsWith("|"))
                    {
                        portName = line.Split('|')[1];
                    }
                }
                file.Close();
            }
            catch (Exception ex)
            {
                ParlaBloccante("il file di configurazione non puo' essere aperto causa: " + ex.Message);
            }
        }


        private void NextPage()
        {
            if (actualIndex < (newsPage.Count - numElementInPage))
            {
                actualIndex += numElementInPage;
                slideStart += numElementInPage;
            }
            else
            {
                actualIndex = 0;
                slideStart = 0;
            }
        }


        private void OpenSerialPort()
        {
            try
            {
                Sp.BaudRate = 9600;
                Sp.Parity = Parity.None;
                Sp.StopBits = StopBits.One;
                Sp.DataBits = 8;
                Sp.Handshake = Handshake.None;
                Sp.DataReceived += SerialPortDataReceived;
                Sp.Open();
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine(ex.Message + ex.StackTrace);
            }
        }


        private void SerialPortDataReceived(object sender, SerialDataReceivedEventArgs e)
        {
            try
            {
                SerialPort sp = (SerialPort)sender;
                string buff = sp.ReadLine();
                if (!String.IsNullOrEmpty(buff))
                {
                    char[] delimiterChars = { ' ' };
                    string[] words = buff.Split(delimiterChars);
                    if (words.Count() == 4)
                    {
                        int a = Convert.ToInt32(words[0].ToString());
                        actualIndex = slideStart + a;
                        if (lastSlideValue != a)
                        {
                            TitoloDaLeggere = true;
                        }
                        lastSlideValue = a;
                        buttonState1 = Convert.ToInt32(words[1].ToString());
                        buttonState2 = Convert.ToInt32(words[2].ToString());
                        buttonState3 = Convert.ToInt32(words[3].ToString());
                    }
                }
            }
            catch
            { 
            }
        }


        private void SelezionaProssimaNews()
        {
            if (actualIndex < newsPage.Count -1)
            {
                actualIndex += 1;
            }
            else
            {
                ParlaBloccante("ultimo elemento");
            }
        }


        private void SelezionaPrecedenteNews()
        {
            if (actualIndex > 0)
            {
                actualIndex -= 1;
            }
            else
            {
                ParlaBloccante("primo elemento");
            }
        }


        private void Wb_DocumentCompleted(object sender, WebBrowserDocumentCompletedEventArgs e)
        {
            string indirizzo = Wb.Url.ToString();
            if (indirizzo != "about:blank")
            {
                if (!lastUrl.StartsWith("http://webvoice.tingwo.co"))
                {
                    string testoHTML = Wb.DocumentText;
                    string percorsoMp3 = RegexLib.FindMp3Path(testoHTML);
                    // download mp3
                    if (percorsoMp3 == "")
                    {
                        if (indirizzo.StartsWith("http://www.ilsole24ore.com"))
                        {
                            if (lastUrl != Wb.Url.ToString())
                            {
                                lastUrl = Wb.Url.ToString();
                                Parla("Lettura articolo");  //in realtà verrà letto al prossimo document_complete
                                Wb.Navigate("http://webvoice.tingwo.co/ilsole5642813vox?url=" + lastUrl);
                            }
                        }
                    }
                    else
                    {
                        Wb.Navigate("about:blank");     // blocca caricamento pagina nel browser
                        WebClient webClient = new WebClient();
                        webClient.DownloadFile("http://webvoice.tingwo.co/" + percorsoMp3, mp3PathFile);//start download
                        StopFile();                     //stop eventualy other file
                        PlayFile(mp3PathFile);     // open mp3file
                        percorsoMp3 = "";               //svuota percorsomp3
                    }
                }
            }
        }


        private void PlayFile(String url)
        {
            Player = new WMPLib.WindowsMediaPlayer();
            Player.PlayStateChange +=
                new WMPLib._WMPOCXEvents_PlayStateChangeEventHandler(Player_PlayStateChange);
            Player.MediaError +=
                new WMPLib._WMPOCXEvents_MediaErrorEventHandler(Player_MediaError);
            Player.URL = url;
            Player.controls.play();
        }


        private void StopFile()
        {
            try
            {
                Player.controls.stop();
                Player.close();
                onPause = false;
                //File.Delete(mp3PathFile);
            }
            catch
            { }
        }


        private void Player_PlayStateChange(int NewState)
        {
            if ((WMPLib.WMPPlayState)NewState == WMPLib.WMPPlayState.wmppsStopped)
            {
                // to do 
                // for eache file save the position and ask if continue from this position on load
                string posizione = Player.controls.currentPositionString;
            }
        }


        private void Player_MediaError(object pMediaObject)
        {
            ParlaBloccante("errore nel caricamento del file");
        }


        private void PauseResumeFile()
        {
            try
            {
                if (onPause)
                {
                    // Pause the Player.
                    Player.controls.play();
                    onPause = false;
                }
                else
                {
                    Player.controls.pause();
                    onPause = true;
                }
            }
            catch
            { }
        }


        private void PlayFeed(int index)
        {
            Wb.Navigate(newsPage[index].SubItems[1].Text);
        }


        private void Form1_KeyDown(object sender, KeyEventArgs e)
        {
            switch (e.KeyCode)
            {
                case Keys.Enter:
                    if (newsPage.Count > 0)
                    {
                        PlayFeed(actualIndex);
                    }
                    break;

                case Keys.Escape:
                    StopFile();
                    Console.Beep();
                    Console.Beep();
                    Console.Beep();
                    this.Close();
                    break;
                case Keys.Down:
                    StopFile();
                    SelezionaProssimaNews();
                    LeggiTitoloNews();
                    break;

                case Keys.Up:
                    StopFile();
                    SelezionaPrecedenteNews();
                    LeggiTitoloNews();
                    break;

                case Keys.Right:
                    StopFile();
                    NextPage();
                    LeggiTitoloNews();
                    break;

                case Keys.Space:
                    PauseResumeFile();
                    break;
            }
        }

        // FAST (but not so elegant) solution for cross threading in serial data input
        private void timer1_Tick(object sender, EventArgs e)
        {
            try
            {
                if (TitoloDaLeggere)
                {
                    LeggiTitoloNews();
                    TitoloDaLeggere = false;
                }
                if (buttonState3 == 0)
                {
                    StopFile();
                    PlayFeed(actualIndex);  // eseguo la lettura dell'articolo
                    buttonState3 = 1;       // resetto la variabile
                }

                if (buttonState2 == 0)
                {
                    PauseResumeFile();      // metto in pausa la lettura dell'articolo
                    buttonState2 = 1;       // resetto la variabile
                }

                if (buttonState1 == 0)
                {
                    StopFile();             // cambio pagina
                    NextPage();
                    LeggiTitoloNews();
                    //resetto la variabile
                    buttonState1 = 1;
                }

            }
            catch
            {
                // in some case, the refresh could cause a delay and throw in error with index

            }
        }

    }
}
