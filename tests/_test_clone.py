import contextlib
import os
import git
import shutil
import tempfile


file_loc = 'bot/languages/localization_any.json'
os.remove(file_loc)

t = tempfile.mkdtemp()

filename = os.path.join(t, 'any_localization.json')
git.Repo.clone_from('https://github.com/lordcod/lordbot-localization', t, branch='addtional-main', depth=1)
shutil.move(filename, file_loc)

with contextlib.suppress(PermissionError):
    shutil.rmtree(t)
