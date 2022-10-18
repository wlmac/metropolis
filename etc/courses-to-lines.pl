#!/bin/env perl

use strict;

chomp;

while (<>) {
	my @row = split ',', $_;
	for (my $i = 0; $i < 4; $i ++) {
		my $code = @row[$i];
		$code =~ s/^\s+//;
		$code =~ s/\s+$//;
		if ($code) {
			printf '{"position": %s, "code": "%s"}', $i, $code;
			print "\n";
		}
	}
}
