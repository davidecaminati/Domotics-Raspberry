/* Programma scritto da Davide Caminati il 3/8/2014
 * davide.caminati@gmail.com
 * http://caminatidavide.it/
 * 
 * licenza copyleft 
 * http://it.wikipedia.org/wiki/Copyleft#Come_si_applica_il_copyleft
 */

// TODO 
// cleanup del codice


/* Example of c:\configfileAudiolibri.txt  the configuration file
@G:\Audiolibri
|COM9
 */


// COMANDI
// ESC per uscire
// INVIO per leggere articolo
// slide per cambiare articolo
// button1 per cambio pagine
// button2 per pause
// button3 per play



using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.IO;
using System.Speech.Synthesis;
using System.IO.Ports;

namespace WindowsFormsApplication1
{
    public partial class Form1 : Form
    {

        // VARIABLES
        bool onPause = false; // variable for trace WindowsMediaPlayer state
        int buttonState1 = 1;
        int buttonState2 = 1;
        int buttonState3 = 1;
        string portName = "";
        List<Libri> BooksList = new List<Libri>();
        List<List<string>> Book = new List<List<string>>();
        List<string> Mp3 = new List<string>();
        List<string> listPath = new List<string>();
        int actualIndexLibro = 0;
        int actualIndexAudio = 0;
        int slideStart = 0;
        int lastSlideValue = 0;
        int IndiceInUso = 0;
        bool TitoloDaLeggere = false;
        int numElementInPage = 7; // Depends on Arduino Slide Settings

        // OBJECTS
        WMPLib.WindowsMediaPlayer Player;
        SerialPort Sp;
        SpeechSynthesizer Synth = new SpeechSynthesizer();

        public Form1()
        {
            InitializeComponent();
            Synth.SetOutputToDefaultAudioDevice();  // Configure the audio output for speech synth. 

            ReadConfigFile();                       // read config (Path, serial port)
            popolaListe();

            Sp = new SerialPort(portName);
        }


        /// <summary>
        /// lettura titolo del libro (viene lanciato automaticamente quando si seleziona un libro)
        /// </summary>
        private void LeggiTitoloLibro(Libri libro)
        {
            //stop eventualy other file
            StopFile();
            try
            {
                Parla(libro.GetName());
            }
            catch
            {
            }
        }


        private void popolaListe()
        {
            foreach (string path in listPath) // must be only one directory
            {
                string[] percorsiLibreria = Directory.GetDirectories(path);
                //append to the elencolibri each foldername finded in the path of the audiolibri
                foreach (string cartella in percorsiLibreria)
                {
                    foreach (string audio in GetListOfFile(cartella))
                    {
                        Mp3.Add(System.IO.Path.GetFileName(audio));
                    }
                    string titolo = System.IO.Path.GetFileNameWithoutExtension(cartella);
                    Libri libro = new Libri(titolo, Mp3);
                    BooksList.Add(libro);
                }

                if (BooksList.Count == 0)
                {
                    ParlaBloccante("errore caricamento libri");
                }
                else
                {

                    LeggiTitoloLibro(BooksList[actualIndexLibro]);
                }
            }
        }


        private void Form1_Load(object sender, EventArgs e)
        {
            //Parla("Audiolibri");
            OpenSerialPort();   // Open the serial port
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
                        actualIndexLibro = slideStart + a;
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


        private void ReadConfigFile()
        {
            try
            {
                string line;
                // Read the configuration file line by line.
                string folder = @System.IO.Path.GetDirectoryName(@System.Reflection.Assembly.GetExecutingAssembly().Location);
                string path_fileconfig = folder + @"\configAudiolibri.txt";
                if (!System.IO.File.Exists(path_fileconfig))
                {
                    //create default file config
                    //first line for directory of the audiolibri directorys
                    string[] lines = { @"G:\Condivisa\Tommasini\Audiolibri", "|COM21" };
                    // WriteAllLines creates a file, writes a collection of strings to the file,
                    // and then closes the file.
                    System.IO.File.WriteAllLines(path_fileconfig, lines);
                }

                System.IO.StreamReader file = new System.IO.StreamReader(path_fileconfig);
                while ((line = file.ReadLine()) != null)
                {
                    if (line.StartsWith("@"))
                    {
                        listPath.Add(line.Split('@')[1]);
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


        private void Muto()
        {
            Synth.SpeakAsyncCancelAll();
        }


        private string[] GetListOfFile(string path)
        {
            return Directory.GetFiles(path);
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
                onPause = false;
            }
            catch
            { }
        }


        private void PauseResumeFile()
        {
            try
            {
                if (onPause)
                {
                    /* Pause the Player. */
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


        private void Player_PlayStateChange(int NewState)
        {
            if ((WMPLib.WMPPlayState)NewState == WMPLib.WMPPlayState.wmppsStopped)
            {
                // to do 
                //for eache file save the position and ask if continue from this position on load
                string posizione = Player.controls.currentPositionString;
            }
        }


        private void Player_MediaError(object pMediaObject)
        {
            Parla("errore nel caricamento del file");
        }


        private void Form1_KeyDown(object sender, KeyEventArgs e)
        {

            switch (e.KeyCode)
            {
                case Keys.Left:

                    StopFile();

                    break;

                case Keys.Space:
                    PauseResumeFile();
                    break;

                case Keys.Down:
                    if (BooksList.Count > 0)
                    {
                        if (BooksList.Count - 1 == BooksList.IndexOf(BooksList[actualIndexLibro]))
                        {
                            Parla("Ultimo elemento");
                        }
                    }
                    break;

                case Keys.Escape:
                    StopFile();
                    Console.Beep();
                    Console.Beep();
                    Console.Beep();
                    this.Close();
                    break;


                case Keys.Enter:
                    if (BooksList.Count > 0)
                    {
                        //find path for mp3 file
                        string percorsofile = Path.Combine(listPath[0], BooksList[actualIndexLibro].GetName(), BooksList[actualIndexLibro].ElencoFiles[actualIndexAudio].ToString());
                        //stop eventualy other file
                        StopFile();
                        // open mp3file
                        PlayFile(percorsofile);
                    }
                    else
                    {
                        Parla("non è possibile caricare i file audio");
                    }
                    break;

                case Keys.Up:
                    StopFile();

                    if (BooksList.Count > 0)
                    {
                        if (0 == actualIndexLibro)
                        {
                            Parla("primo elemento");
                        }
                    }
                    break;
            }
        }


        private void NextPageLibro()
        {
            if (actualIndexLibro < (BooksList.Count - numElementInPage))
            {
                actualIndexLibro += numElementInPage;
                slideStart += numElementInPage;
            }
            else
            {
                actualIndexLibro = 0;
                slideStart = 0;
            }
        }


        private void NextPageAudio()
        {
            if (actualIndexAudio < (BooksList[actualIndexLibro].ElencoFiles.Count - numElementInPage))
            {
                actualIndexAudio += numElementInPage;
                slideStart += numElementInPage;
            }
            else
            {
                actualIndexAudio = 0;
                slideStart = 0;
            }
        }


        private void timer1_Tick(object sender, EventArgs e)
        {
            try
            {
                if (TitoloDaLeggere)
                {
                    LeggiTitoloLibro(BooksList[actualIndexLibro]);
                    TitoloDaLeggere = false;
                }
                if (buttonState3 == 0)
                {
                    StopFile();
                    PlayLibro(actualIndexLibro, actualIndexAudio);  // eseguo la lettura del libro
                    buttonState3 = 1;       // resetto la variabile
                }

                if (buttonState2 == 0)
                {
                    PauseResumeFile();      // metto in pausa la lettura del libro
                    buttonState2 = 1;       // resetto la variabile
                }

                if (buttonState1 == 0)
                {
                    StopFile();             // cambio pagina
                    NextPageLibro();
                    LeggiTitoloLibro(BooksList[actualIndexLibro]);
                    //resetto la variabile
                    buttonState1 = 1;
                }

            }
            catch
            {
                // in some case, the refresh could cause a delay and throw in error with index

            }
        }


        private void PlayLibro(int actualIndexLibro, int actualIndexAudio)
        {
            PlayFile(BooksList[actualIndexLibro].ElencoFiles[actualIndexAudio]);
        }
    }
}
