# Description
This repositoty contains some tools to generate data et configuration files for Nextrain (https://github.com/nextstrain) input 
# Create random metadada and sequence files
To generate random metadata and sequences files, directory structure needs to be as follow

|__ Covid19ScriptsDirectory

       |__ MetadataSimulator.py
			 
       |__ SequenceSimulator.py
			 
|__ config

  		|__ ordering.tsv
					 
|__ data
				
		|__ gisaid_covid19_usa_1759.fasta
						
	User only needs to execute MetadataSimulator.py to create both metadata and sequence files. 
	However, before execution he must change files name accordingly for variables fasta_out and metadata_file. 
	The number of desired sequences is set with variable number_of_isolate. Output files are created in the data directory.
  
  TODO: improvement to come with argparse.
