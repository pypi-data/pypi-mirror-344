import pycantus.data as data

from pycantus import hello_pycantus
hello_pycantus()

from pycantus.models.chant import Chant

chants_file = 'pycantus/dataset_files/sample_dataset/chants.csv' #'../DACT_stuff/data_Mar25/chants_by_genre/A.csv' #all_mar25_chants_no_duplicates.csv' #'scraping/all_mar25_chants.csv'
sources_file = 'pycantus/dataset_files/sample_dataset/sources.csv' #'../DACT_stuff/data_Mar25/all_mar25_sources.csv'


corpus_edit = data.load_dataset(chants_file, sources_file, name='sample', is_editable=True)

print(corpus_edit.chants[0].to_csv_row)
print(corpus_edit.chants[0].header)
print(corpus_edit.all_cids_list())

print(corpus_edit.csv_chants_header)
print()
#print(corpus_edit.csv_sources_header)

#corpus_edit.sources[0].century = None

#print(corpus_edit.sources[0].to_csv_row)
#print(corpus_edit.sources[2])

corpus_edit.chants[0].siglum = 'new_siglum' # should not raise an error
print(corpus_edit.chants[0].to_csv_row) # should have new_siglum

#corpus_edit.sources[2].century = 'nulte' # should not raise an error
#print(corpus_edit.sources[2].to_csv_row) # should have nulte

ch = Chant('005421', 'Ahoj', 'SK-22', 'www.fontes.cz/source', 'www.fontes.cz/chant', '045v', 'FCB')

corpus_edit.chants = [ch]
print(corpus_edit.chants[0].to_csv_row)

corpus_edit.export_csv('chants_export.csv', 'sources_export.csv')

print('\n\nNON EDIT PART')
print()


corpus_non_edit = data.load_dataset('sample_dataset', name='sample', is_editable=False)

print(corpus_non_edit.chants[0].to_csv_row)

# This raises error - great!
#corpus_non_edit.chants[0].locked = True # This should raise an error

# This raises error - great!
#corpus_non_edit.chants[0].siglum = 'new_siglum' # This should raise an error

print(corpus_non_edit.chants[0].siglum) # This should not raise an error


"""
data = Dataset('basic')
data.load()

print(corpus.chants[2].to_csv_row())
print(corpus.sources[0])




# This is what users do

import pycantus.data
cantuscorpus = pycantus.data.load_dataset('cantuscorpus-v0.2', load_editable=True)
my_little_corpus = pycantus.data.load_dataset('my_little_corpus.csv', name='my_little_corpus', **kwargs)

# Alternative for custom data
from pycantus.corpus import Corpus
my_little_corpus = Corpus('my_little_corpus.csv', name='my_little_corpus', **kwargs)


# Now we are in pycantus.data
from pycantus.corpus import Corpus

def _load_available_dataset():
    available_datasets = json.load('static/available_datasets.json')
    return available_datasets
AVAILABLE_DATASET = _load_available_datasets()


def load_dataset(name_or_filepath, **corpus_kwargs):
    if name_or_filepath in AVAILABLE_DATASETS:
        dataset_name = name_or_filepath  # We know we are being asked for a pre-defined corpus.
        dataset_metadata = AVAILABLE_DATASETS[dataset_name]
        corpus = Corpus(**dataset_metadata)
    
    # now we know to expect a custom CSV
    else:
        csv_file_path = name_or_filepath
        corpus = Corpus(csv_file_path, **corpus_kwargs)

    return corpus

# Now we are in pycantus.corpus

class Corpus():
    def __init__(self,
                 expected_csv,
                 fallback_url=None,
                 other_download_parameters=None,
                 is_editable=True,
                 **kwargs):
        
        self.expected_csv = expected_csv
        self.fallback_url = fallback_url
        self.kwargs = kwargs
        self.is_editable = is_editable

        # This is in fact going in a loader.
        if not os.path.isfile(expected_csv):
            if not self.fallback_url:
                raise ValueError('Non-existent chant CSV file specified.')
            chants, sources = self._load_from_fallback_url(url=self.fallback_url, target=self.expected_csv)
        else:
            chants, sources = self._simple_load_from_csv(expected_csv)

        self._chants = chants
        self._sources = sources

        if not self.is_editable:
            self._lock_chants()
            self._lock_sources()
    
    @property.getter
    def chants(self):
        return self._chants
    
    @property.setter
    def chant(self, new_chants):
        if self.is_editable:
            self._chants = new_chants
        else:
            raise KeyError('Corpus is not editable, cannot replace chant list.')
    
    def _lock_chants(self):
        for c in self._chants:
            c.locked = True

    def _lock_sources(self):
        for s in self._sources:
            s.locked = True


"""