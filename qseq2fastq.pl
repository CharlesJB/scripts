#!/usr/bin/perl
# From: http://seqanswers.com/forums/showthread.php?t=1655
# Note: Need to rename file to: s_1_1_0001_qseq.txt
use strict;
use Carp;
generate_sequence_list(".", 1, 1, "output.fastq"); # where "0" means single end and "8" means lane 8


# **** begin code ****
sub generate_sequence_list {
    # **** BEGIN CONFIG OPTIONS ****
    my $bustard_path = $_[0];
    my $pair = $_[1]; # 0=single end, 1=first pair, 2=second pair
    my $lane = $_[2];
    my $output_fastq_file = $_[3];
    # **** END CONFIG OPTIONS ****

    my $this_tile = 1;
    my $qfilter = "";

    open(OUTFASTAQFILE, "> $output_fastq_file");

    if($pair > 0){
        $pair = "_" . $pair . "_" ;
    } else {
        $pair = "_1_";
    }

    printf($bustard_path . "/s_" . $lane . $pair . sprintf("%04d", $this_tile) . "_qseq.txt\n");
    while(-r $bustard_path . "/s_" . $lane . $pair . sprintf("%04d", $this_tile) . "_qseq.txt"){
        my $filename = $bustard_path . "/s_" . $lane . $pair . sprintf("%04d", $this_tile) . "_qseq.txt";
        open(INFILE, "< $filename");
        foreach my $thisline (<INFILE>) {
            my @this_line = split("\t", $thisline);
            croak("Error: invalid column number in $filename\n") unless(scalar(@this_line) == 11);
            if($this_line[10] == 1) {
                $qfilter = "Y";
            } else {
                $qfilter = "N";
            }
            # Convert quality scores
            my $quality_string = $this_line[9];
            my @quality_array = split(//, $quality_string);
            my $phred_quality_string = "";
            # convert each char to Phred quality score
            foreach my $this_char (@quality_array){
                my $phred_quality = ord($this_char) - 64; # convert illumina scaled phred char to phred quality score
                my $phred_char = chr($phred_quality + 33); # convert phred quality score into phred char
                $phred_quality_string = $phred_quality_string . $phred_char;
            }

            # replace "." gaps with N
            $this_line[8] =~ s/\./N/g;

            # output line
            print OUTFASTAQFILE "@" . $this_line[2] . ":" . $this_line[3] . ":" . # output label line
            $this_line[4] . ":" . $this_line[5] . ":" . $qfilter . "\n" .
            $this_line[8] . "\n+\n" . # output sequence
            $phred_quality_string . "\n"; # output quality string
        }
        close(INFILE);
        $this_tile++;
    }
    $this_tile--;
    croak("Error: 99 or less tiles in lane\n") unless($this_tile > 99);
    print "\tFound $this_tile tiles in lane $lane.\n";

    close(OUTFASTAQFILE);
}
# **** end code ****
