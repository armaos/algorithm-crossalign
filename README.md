This card outlines what is needed to get CROSS image and algorithm working locally.

Most of the steps will be Mac-specific and assume that you have installed docker engine (https://docs.docker.com/engine/installation/mac/) and running docker-machine as a virtualbox VM (managed transparently by the docker toolkit)

Download the docker image with the installed dependencies for algorithm cross to run.

>$docker pull tartaglialab/algorithm_cross

Clone the source code of the algorithm from our git repository in a folder of your preference.

>$git clone https://github.com/crg-bioinformatics-genomics/algorithm-cross.git

Create a submission folder for your example

Directory structure you need to have:

>/repositories/algorithm-cross

>/repositories/processor/work_in_progress/submissions/2016-06/test/output/

Example for 
>Global run

>G1intas
CUCAUAUUUCGAUGUGCCUUGCGCCGGGAAACCACGCAAGGGAUGGUGUCAAAUUCGGCGAAACCUAAGCGCCCGCCCGGGCGUAUGGCAACGCCGAGCCAAGCUUCGGCGCCUGCGCCGAUGAAGGUGUAGAGACUAGACGGCACCCACCUAAGGCAAACGCUAUGGUGAAGGCAUAGUCCAGGGAGUGGCGAAAGUCACACAAACCGGAAUC

Run the exact command:

>$docker run -v /the_complete_path_to_/repositories/:/repositories/  -t -i -w='/repositories/processor/' tartaglialab/algorithm_cross  ../algorithm-cross/cross.py -output_dir="work_in_progress/submissions/2016-06/test/output/" -FORMfeature="global" -FORMsequence_one=">G1intas
CUCAUAUUUCGAUGUGCCUUGCGCCGGGAAACCACGCAAGGGAUGGUGUCAAAUUCGGCGAAACCUAAGCGCCCGCCCGGGCGUAUGGCAACGCCGAGCCAAGCUUCGGCGCCUGCGCCGAUGAAGGUGUAGAGACUAGACGGCACCCACCUAAGGCAAACGCUAUGGUGAAGGCAUAGUCCAGGGAGUGGCGAAAGUCACACAAACCGGAAUC"


Your result would be in
>repositories/processor/work_in_progress/submissions/2016-06/test/output/
