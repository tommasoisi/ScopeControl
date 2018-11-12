
#!/bin/bash

FNAL_SCOPE_DIR=/eos/cms/store/group/phys_susy/razor/FNAL_TB_1811/Scope_standalone

done_runs=($(ls -d ${FNAL_SCOPE_DIR}/ROOT/*.root))
new_runs=($(ls -dt ${FNAL_SCOPE_DIR}/RAW/*))
# for (( run_i=0; run_i<${#new_runs[@]}; run_i++ ));
# do
#   echo ${new_runs[$run_i]}
# done

lenDone=${#done_runs[@]}
lenNew=${#new_runs[@]}
let lenToDo=$lenNew-$lenDone
echo Processing $lenToDo new files

for (( run_i=0; run_i<$lenToDo; run_i++ ));
do
  python conversion.py ${new_runs[$run_i]}
done
