# This file is part of the Frescobaldi project, http://www.frescobaldi.org/
#
# Copyright (c) 2011 by Wilbert Berendsen
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# See http://www.gnu.org/licenses/ for more information.

"""
All completions data.
"""

from __future__ import unicode_literals

import itertools

import listmodel
import ly.words
import ly.data

from . import util


# some groups of basic lilypond commands

# markup (toplevel, book and bookpart)
markup = (
    'markup',
    'markuplines',
    'pageBreak',
    'noPageBreak',
)

# these can occur (almost) everywhere
everywhere = (
    'language',
    'pointAndClickOn',
    'pointAndClickOff',
    'include',
)

# commands that change input mode, can introduce a music expression
inputmodes = (
    'chords',
    'chordmode {',
    'drums',
    'drummode {',
    'figures',
    'figuremode {',
    'lyrics',
    'lyricmode {',
    'addlyrics {',
)

# commands that only occur at the global file level
toplevel = (
    'version',
    'sourcefileline',
    'sourcefilename',
)

# other commands that can start a music expression
start_music = (
    'repeat',
    'alternative {',
    'relative',
    'transpose',
    'partcombine',
    'keepWithTag #\'',
    'removeWithTag #\'',
    'new',
    'context',
    'with',
)

# tweak commands may be assigned, in toplevel
tweaks = (
    'once',
    'override',
    'revert',
    'set',
    'unset',
)

# modes book, bookpart and score
modes = (
    'book {',
    'bookpart {',
    'score {',
)

# blocks: paper, header, layout
blocks = (
    'paper {',
    'header {',
    'layout {',
)

# commands that are used in context definitions
cmds_context = (
    'override',
    'consists',
    'remove',
    'RemoveEmptyStaves',
    'accepts',
    'alias',
    'defaultchild',
    'denies',
    'name',
)

# in \with { } a smaller set
cmds_with = cmds_context[:3]


lilypond_markup = listmodel.ListModel(['\\markup'])

lilypond_markup_commands = listmodel.ListModel(
    sorted(ly.words.markupcommands),
    display = util.command)

lilypond_header_variables = listmodel.ListModel(
    sorted(ly.words.headervariables), edit = util.variable)

lilypond_paper_variables = listmodel.ListModel(
    sorted(ly.words.papervariables), edit = util.variable)

lilypond_layout_variables = listmodel.ListModel(
    ['\\context {',] + sorted(ly.words.layoutvariables),
    edit = util.cmd_or_var)

lilypond_contexts = listmodel.ListModel(sorted(ly.words.contexts))

lilypond_grobs = listmodel.ListModel(ly.data.grobs())

lilypond_contexts_and_grobs = listmodel.ListModel(
    sorted(ly.words.contexts) + ly.data.grobs())

lilypond_context_properties = listmodel.ListModel(
    ly.data.context_properties())

lilypond_contexts_and_properties = listmodel.ListModel(
    sorted(ly.words.contexts) + ly.data.context_properties())

lilypond_context_contents = listmodel.ListModel(sorted(itertools.chain(
    util.make_cmds(ly.words.contexts),
    ly.data.context_properties(),
    util.make_cmds(cmds_context),
    )), edit = util.cmd_or_var)

lilypond_with_contents = listmodel.ListModel(sorted(itertools.chain(
    ly.data.context_properties(),
    util.make_cmds(cmds_with),
    )), edit = util.cmd_or_var)

lilypond_toplevel = listmodel.ListModel(sorted(
    toplevel + everywhere + inputmodes + markup + start_music + tweaks
    + modes + blocks
    ), display = util.command)

lilypond_book = listmodel.ListModel(sorted(
    everywhere + inputmodes + markup + start_music
    + modes[1:] + blocks + (
    'bookOutputName',
    'bookOutputSuffix',
    )), display = util.command)

lilypond_bookpart = listmodel.ListModel(sorted(
    everywhere + inputmodes + markup + start_music + modes[2:] + blocks
    ), display = util.command)
    
lilypond_score = listmodel.ListModel(sorted(
    everywhere + inputmodes + start_music + blocks[1:] + (
    'midi {',
    )), display = util.command)

lilypond_engravers = listmodel.ListModel(ly.data.engravers())
    
def lilypond_grob_properties(grob):
    return listmodel.ListModel(ly.data.grob_properties(grob),
        display = lambda item: "#'" + item)

lilypond_all_grob_properties = listmodel.ListModel(ly.data.all_grob_properties(),
    display = lambda item: "#'" + item)

lilypond_markup_properties = listmodel.ListModel(
    sorted(set(sum(map(ly.data.grob_interface_properties, (
        # see lilypond docs about \markup \override
        'font-interface',
        'text-interface',
        'instrument-specific-markup-interface',
    )), []))))

lilypond_modes = listmodel.ListModel(ly.words.modes, display = util.command)

lilypond_clefs = listmodel.ListModel(ly.words.clefs_plain)

lilypond_repeat_types = listmodel.ListModel(ly.words.repeat_types)
