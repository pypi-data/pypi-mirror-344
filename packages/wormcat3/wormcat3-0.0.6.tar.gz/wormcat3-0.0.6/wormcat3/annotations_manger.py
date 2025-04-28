import pandas as pd
import os
from wormcat3 import file_util
import wormcat3.constants as cs

class AnnotationsManager:
    """ Manages gene annotations and preprocessing. """
    
    def __init__(self, annotation_file=cs.DEFAULT_ANNOTATION_FILE_NAME):
        """Initialize with the path to the annotation file."""
        if file_util.is_file_path(annotation_file):
            self.annotation_file_path = annotation_file
        else:
            self.annotation_file_path = file_util.find_file_path(annotation_file)
            if not self.annotation_file_path:
                raise FileNotFoundError(f"Annotation file not found: {annotation_file}")
                        
        self.annotations_df = self._load_annotations()
            
     
        
    def _load_annotations(self):
        """ Load annotations from file. """
        
        try:
            df = pd.read_csv(self.annotation_file_path)
            df.columns = df.columns.str.replace(' ', '.')
            if df.empty:
                raise ValueError(f"Annotation file '{self.annotation_file_path}' is empty.")
            return df
        except Exception as e:
            raise ValueError(f"Failed to load annotation file: {e}")
    
    def get_gene_id_type(self, gene_set):
        """ Determine the gene ID type from the gene set. """
        
        if len(gene_set) < 2:
            raise ValueError("At least two genes are required for comparison.")
        
        # Check if the first two genes start with "WBGene"
        if gene_set[0].startswith("WBGene") and gene_set[1].startswith("WBGene"):
            return "Wormbase.ID"
        elif not gene_set[0].startswith("WBGene") and not gene_set[1].startswith("WBGene"):
            return "Sequence.ID"
        else:
            raise ValueError("Invalid gene data: One gene starts with 'WBGene', but the other does not.")
    
    @staticmethod
    def dedup_list(input_list):
        """ Deduplicate a list while preserving order. """
        
        seen = set()
        deduped_list = []
        for item in input_list:
            if item not in seen:
                deduped_list.append(item)
                seen.add(item)
        return deduped_list
    
    def add_annotations(self, gene_set_list, gene_type):
        """ Add annotations to the gene set. """
        
        gene_set_df = pd.DataFrame(gene_set_list, columns=[gene_type])
        
        # Verify if 'gene_type' is a column in the DataFrame
        if gene_type not in self.annotations_df.columns:
            raise ValueError(f"Column '{gene_type}' not found in the DataFrame.")
        
        return pd.merge(gene_set_df, self.annotations_df, on=gene_type, how='left')


    def segment_genes_by_annotation_match(self, gene_set_list, gene_type):
        """ Split background genes into those with and without annotations. """
        
        gene_set_df = pd.DataFrame(gene_set_list, columns=[gene_type])
        
        # Check if gene_type is in both dataframes
        if gene_type not in gene_set_df.columns:
            raise ValueError(f"'{gene_type}' not found in gene_set_df.")
        if gene_type not in self.annotations_df.columns:
            raise ValueError(f"'{gene_type}' not found in annotations_df.")
        
        # Perform the left merge
        merged_df = pd.merge(gene_set_df, self.annotations_df, on=gene_type, how='left')
        
        # Split based on presence of annotation (assuming at least one non-key column in annotations_df)
        annotation_columns = [col for col in self.annotations_df.columns if col != gene_type]
        
        genes_matched_df = merged_df.dropna(subset=annotation_columns)
        genes_not_matched_df = merged_df[merged_df[annotation_columns].isnull().all(axis=1)]
        genes_not_matched_df = genes_not_matched_df[[gene_type]]

        return genes_matched_df, genes_not_matched_df

    def create_gmt_for_annotations(self, output_dir_path, output_file_nm_prefix="wormcat"):
        """ Create GMT formatted files for all categories. """
        for category in [1,2,3]:
            gmt_format = self.category_to_gmt_format(category)
            output_file_path = f"{output_dir_path}/{output_file_nm_prefix}_cat_{category}.gmt"
            self.save_gmt_to_file(gmt_format, output_file_path)    

    def category_to_gmt_format(self, category):
        """ Convert an annotation dataframe category to GMT format. """
        category_col = f"Category.{category}"
        gene_col = "Wormbase.ID"
        id_col = "Function.ID"
                
        category_df = self.annotations_df[[gene_col, category_col]]
        category_df = category_df.rename(columns={category_col: id_col})
        
        # Validate that required columns exist
        required_cols = [id_col, gene_col]        
        missing_cols = [col for col in required_cols if col not in category_df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")
        
        # Assert ID column has no NaN values
        assert not category_df[id_col].isna().any(), f"Column '{id_col}' contains NaN values"
        
        # Use ID column as description if desc_col is None
        grouped = category_df.groupby([id_col])[gene_col].apply(list).reset_index()
        
        # Assert there's at least one gene set
        assert len(grouped) > 0, "No gene sets found after grouping"
        
        # Create GMT formatted dictionary
        gmt_format = {}
        for _, row in grouped.iterrows():            
            # Filter out any None or NaN values from gene list
            gene_list = [str(gene) for gene in row[gene_col] if pd.notna(gene)]
            
            # Only include if there are genes in the set
            if gene_list:
                gmt_format[row[id_col]] = gene_list
        
        # Final assertion to ensure data was processed
        assert len(gmt_format) > 0, "No gene sets were generated"
        
        return gmt_format

    def save_gmt_to_file(self, gmt_format, output_file_path='wormcat.gmt'):
        """ Write GMT formatted dictionary to disk. """
        # Ensure the output directory exists
        output_dir_path = os.path.dirname(output_file_path)
        file_util.validate_directory_path(output_dir_path, not_empty_check = False) 
        
        # Write to GMT file
        with open(output_file_path, 'w') as file:
            for gene_id, gene_list in gmt_format.items():
                description = gene_id
                line = f"{gene_id}\t{description}\t" + '\t'.join(gene_list)
                file.write(line + '\n')
        
        # Final assertions to ensure data was written
        assert os.path.exists(output_file_path), f"Output file {output_file_path} was not created"
        assert os.path.getsize(output_file_path) > 0, f"Output file {output_file_path} is empty"
        
        print(f"Successfully created GMT file: {output_file_path}")
        
        return output_file_path
