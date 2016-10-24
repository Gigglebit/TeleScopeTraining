#!/usr/bin/perl -w


#open F,"<","17To19noonRefined";
open F,"<","1006To1011Refined";

@lines = <F>;

close F;

open F2,">","1006To1011MergeToOneEntry";


while($#lines>5){
	##the duration field should be in increasing order
	##this eliminate the repeated entry as well
	@tempArr0 = split(',',$lines[0]) ;
	@tempArr1 = split(',',$lines[1]) ;
	if($tempArr0[5]<$tempArr1[5]){
		@tempArr2 = split(',',$lines[2]) ;
		if($tempArr1[5]<$tempArr2[5]){
			@tempArr3 = split(',',$lines[3]) ;
			if($tempArr2[5]<$tempArr3[5]){
				@tempArr4 = split(',',$lines[4]) ;
				if($tempArr3[5]<$tempArr4[5]){
					@tempArr5 = split(',',$lines[5]) ;
					if($tempArr4[5]<$tempArr5[5]){
						@tempArr6 = split(',',$lines[6]) ;	
						if($tempArr5[5]<$tempArr6[5]){
							@outputArray = (@tempArr0[0..4],@tempArr1[0..4],@tempArr2[0..4],@tempArr3[0..4],@tempArr4[0..4],@tempArr5[0..4],@tempArr6[0..4]);
							push @outputArray,$tempArr6[6];
							$outputString = join(",",@outputArray);
							#print $outputString,"\n";
							print F2 $outputString;
							@outputArray=();
							$outputString="";
							shift @lines;
							shift @lines;
							shift @lines;	
							shift @lines;
							shift @lines;
							shift @lines;
							shift @lines;
							next;
						}else{
							shift @lines;
							shift @lines;
							shift @lines;	
							shift @lines;
							shift @lines;
							shift @lines;
							next;
						}
					}else{
						shift @lines;
						shift @lines;
						shift @lines;	
						shift @lines;
						shift @lines;
						next;
					}
				}else{
					shift @lines;
					shift @lines;
					shift @lines;	
					shift @lines;
					next;				
				}
		
			}else{
				shift @lines;
				shift @lines;
				shift @lines;
				next;
			}
		}else{
			shift @lines;
			shift @lines;
			next;
		}
	}else{
		shift @lines;
		next;
	}

}

close F2;

