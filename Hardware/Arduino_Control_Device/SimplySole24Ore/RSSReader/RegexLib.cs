using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;

namespace RSSReader
{
     class RegexLib
    {
        public static string FindMp3Path(string input)
        {
            string pattern = @"[""].download.+[""]";
            Regex rgx = new Regex(pattern, RegexOptions.Compiled | RegexOptions.IgnoreCase);

            // Find matches.
            MatchCollection matches = rgx.Matches(input);
            string risultato = "";
            if (matches.Count == 1)
            {
                risultato = matches[0].ToString();
                risultato = risultato.Replace("\"", "");
            }
            return risultato;
        }
    }
}
