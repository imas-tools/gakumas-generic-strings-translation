from arrange import arrange
from utils import get_kvs_for_dir, translation_dir, working_new_dir

def apply():
    kvs = get_kvs_for_dir(translation_dir)
    kvs.update(
        get_kvs_for_dir(working_new_dir)
    )
    arrange(kvs)

if __name__ == '__main__':
    apply()
