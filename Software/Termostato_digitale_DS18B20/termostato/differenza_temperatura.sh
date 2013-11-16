#!/usr/bin/perl -w

use strict;
use LWP::Simple;

my $url = "http://www.wunderground.com/cgi-bin/findweather/getForecast?"
        . "query=";
my $ca = get("${url}cesena"); # cesena, italia
#my $ma = get("${url}02140"); # Cambridge, Massachusetts
print $ca;
my $ca_temp = current_temp($ca);
#my $ma_temp = current_temp($ma);
#my $diff = $ca_temp - $ma_temp;
print $ca;
#print $diff > 0 ? "California" : "Massachusetts";
#print " is warmer by ", abs($diff), " degrees F.\n";
print "California";

sub current_temp {
  local $_ = shift;
  m{<tr ><td>Temperatura</td>\s+<td><b>(\d+)} || die "No temp data?";
  return $1;
}
