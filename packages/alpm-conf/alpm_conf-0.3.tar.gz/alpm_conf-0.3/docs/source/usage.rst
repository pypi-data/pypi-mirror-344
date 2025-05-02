Usage
=====

*alpm-conf* is run with the subcommands ``help``, ``create``, ``update`` or
``sync``.

Help on a subcommand is printed by::

  $ alpm-conf help <subcommand>

The :ref:`alpm-conf` lists the options available for each subcommand.

*alpm-conf* does not need to be run within its git repository, however conflicts
must be resolved and commited within the repository.

.. _terminology:

Terminology
-----------

etc-file
    The path name of a file within the /etc directory excluding the leading
    ``/``.

user-file
    An *etc-file* that has been created by the *root* user (such as a *netctl*
    profile) in the /etc directory.

cherry-pick
    The *cherry-pick* list is the list of ``new`` [#]_ *etc-files* extracted
    from new versions of package archives that are different from the
    ``original`` files in the previous version and that have been modified by
    the *root* user in the ``current`` instanciation in the /etc directory. The
    *cherry-pick* list is commited on the *etc-tmp* branch and the changes made
    by this commit are applied by the ``git cherry-pick`` command to the
    *master-tmp* branch.

Git repository
--------------

The *master-tmp*, *etc-tmp* and *packages-tmp* temporary branches are created by
the *update* command at respectively the *master*, *etc* and *packages*
branches. The changes made by this command are made in the temporary
branches. These branches are merged into their ancestor as a fast-forward
merge by the *update* command when the *cherry-pick* list is empty or by the
*sync* command otherwise. The temporary branches are removed after the merge.

*master* branch
    * The *etc-files* installed by pacman and modified by the *root* user.
    * The *user-files*.

*etc* branch
    The *etc-files* of the package archives currently installed.

*packages* branch
    The files whose names are the names of the packages currently
    installed. Each file contains the package version and the sha256 of their
    *etc-files*.

The *master-prev*, *etc-prev* and *packages-prev* tags are created at
their respective branch just before the fast-forward merge.

create command
--------------

Create the git repository and populate the *master* branch with files
installed by pacman in the /etc directory that have been modified by the *root*
user. The command may be issued by the *root* user or by a plain user, the next
*alpm-conf* commands should be issued by the owner of the repository except for
the :ref:`sync cmd`.

The git repository is located at the directory specified by the
command line option ``--gitrepo-dir`` when this option is set, otherwise
at $XDG_DATA_HOME/alpm-conf if the XDG_DATA_HOME environment variable
is set, otherwise at $HOME/.local/share/alpm-conf.

.. note::
   An *etc-file* added to the *master* branch by this command may have been
   modified in the /etc directory a long time ago and never updated since
   then. The file may be very different from the one in the latest package
   version. In that case, when a new version of this file is installed by
   pacman, the following *update* command may fail to merge the changes and
   trigger a :ref:`conflict` because the file in the *master* branch originates
   from a too old version. The conflict must be resolved manually.

update command
--------------

Update the *master-tmp* branch or the *master* branch in the following cases:

 * after a pacman update,
 * after modifications by the *root* user of pacman installed *etc-files*,
 * after modifications of *user-files* when these files are tracked by the
   *master* branch.

When the *cherry-pick* list is empty, the changes are made in the *master*
branch (after the merge of the temporary branches and their removal) and there
is nothing to sync to the /etc directory.

Otherwise the changes are made in the *master-tmp* branch and those changes that
were made in the *cherry-pick* list need to be copied to the /etc directory
with the *sync* command. At
this stage (before the *sync* command) it is still possible to run another
*update* command even after the context in which the previous command was run
has changed (new pacman update, new modifications in files on /etc).

.. _`conflict`:

Cherry-pick conflict
""""""""""""""""""""

The ``git cherry-pick`` command that is run by the *update* command in order to
apply the changes made in the *etc-tmp* branch to the *master-tmp* branch may
fail with conflict(s). In that case the *update* command terminates and prints
the list of files that need to resolved in the *master-tmp* branch that is
currently checked out.

To complete the *update* command one must:

 * Change the working directory to the git repository.
 * Resolve the conflict(s) using ``git merge`` or ``git mergetool``.
 * Commit the changes.
 * Possibly check the changes that have been made with the command::

    $ git diff master...master-tmp

 * Run the *sync* command.

.. _`sync cmd`:

sync command
------------

Copy the changes made in the *cherry-pick* list afer an *update* command from
the *master-tmp* branch to the /etc directory.

The command must be made with *root* privileges. When the *alpm-conf* user is a
plain user it may be useful to run the ``sudo`` or ``su`` command while
preserving the user's environment. This is done with the following command line
arguments:

 * sudo
     *-E* or *--preserve-env*

 * su
     *-m* or *-p* or *--preserve-environment*

Checking with git
-----------------

The following commands must be run within the git repository.

List the *user-file* names (see :ref:`terminology`)::

    git diff-tree -r --name-only --diff-filter=A etc master --

Print the changes before a *sync* command::

    $ git diff master...master-tmp

Print the changes after a *sync* command or an *update* command, that is after
the temporary branches have been merged and removed::

    $ git diff master-prev...master

Print the differences between the *master* branch and the *etc-files* of
the package archives currently installed by pacman::

    $ git diff etc master --

Print the difference between one *etc-file* (for example ``etc/pacman.conf``)
in the *master* branch and the version of this file in the installed package
archive::

    $ git diff etc master -- etc/pacman.conf

emacs git tools
---------------

Here is one of the ways to configure git to use emacs as a git tool. Adding the
following lines to ``$HOME/.gitconfig`` allows to use emacs to run ``git ediff``
in place of the *git diff* command and ``git mergetool`` in place of the *git
merge* command::

  [diff]
      tool = ediff-difftool

  [difftool "ediff-difftool"]
      prompt = false
      cmd = emacs --no-desktop --eval \"(ediff-directories\
              \\\"$LOCAL\\\" \\\"$REMOTE\\\" nil)\" \
              2>/dev/null

  [merge]
      tool = ediff-mergetool

  [mergetool "ediff-mergetool"]
      keepBackup = false
      trustExitCode = true
      cmd = emacs --no-desktop --eval \"(ediff-merge-files-with-ancestor\
              \\\"$LOCAL\\\" \\\"$REMOTE\\\" \\\"$BASE\\\" nil \\\"$MERGED\\\")\" \
              2>/dev/null

  [alias]
      ediff = difftool -d

.. rubric:: Footnotes

.. [#] Using the terminology of the **HANDLING CONFIG FILES** section in the
       pacman man page.
