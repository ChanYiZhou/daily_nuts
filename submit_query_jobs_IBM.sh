#submit post 
cd $case_path 
echo "llsubmit $submit_post"
llsub="`llsubmit $submit_post`"
#echo "##llsub=$llsub##"
jobid=`echo $llsub | cut -d\" -f4`
echo "post is submit...jobid= $jobid"
strq=" "
i=0 
while true ;do
	strq="`llq  $jobid -X cl_cmb`"
	substr="llq: There is currently no job status to report"	
	#echo "loop i= $i"
	#echo "strq=$strq"
	if [[ $strq =~ $substr ]] ;then
	   		break	
	fi
	echo "sleep 1 minters"
	sleep 60
	((i++))
done
echo "---------------------------------------"
echo " Regcm post  done  successfully!"
echo "---------------------------------------"
