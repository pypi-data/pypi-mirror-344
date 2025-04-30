import data
from models.chant import Chant

ch = Chant('005421', 'Ahoj', 'SK-22', 'www.fontes.cz/source', 'www.fontes.cz/chant', '045v', 'FCB')

chants_file = 'scraping/sample_chants.csv' #'scraping/all_mar25_chants.csv'
sources_file = 'scraping/sample_sources.csv'


corpus_edit = data.load_dataset(chants_file, sources_file, name='sample', is_editable=True)

print(corpus_edit.chants[0].to_csv_row())
print(corpus_edit.chants[0].get_header())

print(corpus_edit.sources[0].to_csv_row())
print(corpus_edit.sources[2])

corpus_edit.chants[0] = ch
print(corpus_edit.chants[0].to_csv_row())

print()
print(corpus_edit.chants[1].to_csv_row())
corpus_edit.chants[1].cantus_id = '123ukazkaCID'
print(corpus_edit.chants[1].to_csv_row())

print()


# NON EDITABLE TESTING
corpus_non_edit = data.load_dataset('sample_dataset', name='sample', is_editable=False)

print(corpus_non_edit.chants[0].to_csv_row())
corpus_non_edit.chants[0] = ch
print(corpus_non_edit.chants[0].to_csv_row())

print()
print(corpus_non_edit.chants[1].to_csv_row())
corpus_non_edit.chants[1].cantus_id = '123ukazkaCID'
print(corpus_non_edit.chants[1].to_csv_row())


#corpus_download = data.load_dataset('cantuscorpus-v0.2', name='cantuscorpus-v0.2', is_editable=False)
#print(corpus_download.chants[0].to_csv_row())

#corpus_whole = data.load_dataset('scraping/all_mar25_chants_no_duplicates.csv', name='all_mar_25', is_editable=True)




"""

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