#! /usr/local/bin/perl -w


#################################################################################
#										#
#  										#
#   ASCII Resolve v.0.1								#
#   Copyright (C) 2003-2004 - Steven Schubiger <steven@accognoscere.org>	#
#   Last changes: 14th November 2004						#
#										#
#   This program is free software; you can redistribute it and/or modify	#
#   it under the terms of the GNU General Public License as published by	#
#   the Free Software Foundation; either version 2 of the License, or		#
#   (at your option) any later version.						#
#										#
#   This program is distributed in the hope that it will be useful,		#
#   but WITHOUT ANY WARRANTY; without even the implied warranty of		#
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the		#
#   GNU General Public License for more details.				#
#										#
#   You should have received a copy of the GNU General Public License		#
#   along with this program; if not, write to the Free Software			#
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA	#
#										#
#										#
#################################################################################




# Include the configuration file
require 'ascii-resolv.cfg';

use CGI;
my $query = new CGI;
my $action = $query->param('action');
my $user_input = $query->param('user_input');


# Launch the main functions
unless ($action) {
    &parse_template();
    &print_form();
} 
elsif ($action eq 'ascii_resolv') {
    &calculate_ascii();
    &parse_template();
    &parse_config_format();
    &print_form();
}


# Parse the HTML template & split its content in several variables
sub parse_template {
    open (TEMPLATE, "<$template") or die "Could not open $template: $!\n";
    while (! eof(TEMPLATE) ) {
        $template_html .= <TEMPLATE>;
    }
    close (TEMPLATE) or die "Could not close $template: $!\n";

    $template_head = $template_html;
    $template_body = $template_html;
    $template_footer = $template_html;

    $template_head =~ s/\n/newline/g;
    $template_body =~ s/\n/newline/g;
    $template_footer =~ s/\n/newline/g;

    $template_head =~ s/(.*)<tr.*/$1/;
    $template_body =~ s/.*(<tr.*?<\/tr>).*/$1/;
    $template_footer =~ s/.*<\/tr.*?>(.*)/$1/;

    $template_head =~ s/newline/\n/g;
    $template_body =~ s/newline/\n/g;
    $template_footer =~ s/newline/\n/g;
} 


# Parse the config format file input
sub parse_config_format {
    open (CONFIG_FORMAT_FILE, "<$config_format_file") or die "Could not open $config_format_file: $!\n";
    
    for ($i = 0; $i < 18; $i++) {
        $crap = <CONFIG_FORMAT_FILE>;
    }
    while (my $line = <CONFIG_FORMAT_FILE>) {
        if ($line !~ /\#/) {
            $ascii_resolv_format .= $line;
        } 
        else { last }
    }

    close (CONFIG_FORMAT_FILE) or die "Could not close $config_format_file: $!\n";
}


# Print the HTML form
sub print_form {
    print "Content-type: text/html\n\n";
    $template_head =~ s/\$SCRIPT_URL/$script_url/i;
    print $template_head;

    unless (defined( $action )) {
        $template_body =~ s/\$RESOLV_ASCII//;
        print $template_body;
    } 
    elsif ($action eq 'ascii_resolv') {
        my @keys = keys %table;
        my @sorted_keys = sort {$a <=> $b} @keys;

        foreach my $key (@sorted_keys) {
            my $template_body_in_use = $template_body;

            my $ascii_resolv_format_in_use = $ascii_resolv_format;
            $ascii_resolv_format_in_use =~ s/\$DIGIT/$key/;
            $ascii_resolv_format_in_use =~ s/\$ASCII/$table{$key}/;

            $template_body_in_use =~ s/\$RESOLV_ASCII/$ascii_resolv_format_in_use/;
            print $template_body_in_use;
       }
    }
     
    print $template_footer;
    exit (0);
}
    

# Calculate the ASCII codes; either from 1-255 or an user input.
sub calculate_ascii {
    if ($user_input =~ /\d+/ && ($user_input < 0 || $user_input > 255)) {
        &print_form ($user_input_failed);
    }
    unless ($user_input =~ /\w+/ || $user_input =~ /\d+/ || $user_input =~ /\s+/) {
        for ($i = 1; $i <= 255; $i++) {
            $table{$i} = chr( $i );
        }
    } 
    else {
        if ($user_input !~ /\d+/) {
            my $i = ord( $user_input );
            $table{$i} = $user_input;
        } 
        else {
            my $ascii = chr( $user_input );
            $table{$user_input} = $ascii;
        }
    }
}