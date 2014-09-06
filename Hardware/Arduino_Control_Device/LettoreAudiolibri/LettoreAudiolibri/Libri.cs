using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace WindowsFormsApplication1
{
    class Libri
    {
        public List<string> ElencoFiles;
        private string _titolo;

        // Default constructor:
        public Libri(string titolo, List<string> elencofile)
        {
            _titolo = titolo;
            ElencoFiles = elencofile;
        }

        // Printing method:
        public string GetName()
        {
            return _titolo;
        }

    }
}
