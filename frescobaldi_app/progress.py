# This file is part of the Frescobaldi project, http://www.frescobaldi.org/
#
# Copyright (c) 2008 - 2012 by Wilbert Berendsen
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
Manages the progress bar in the status bar of ViewSpaces.
"""

from __future__ import unicode_literals

from PyQt4.QtCore import Qt, QTimeLine, QTimer
from PyQt4.QtGui import QProgressBar

import app
import plugin
import jobmanager
import metainfo
import widgets.progressbar

metainfo.define('buildtime', 0.0, float)


class ProgressBar(plugin.ViewSpacePlugin):
    """A Simple progress bar to show a Job is running."""
    def __init__(self, viewSpace):
        bar = self._bar = widgets.progressbar.TimedProgressBar()
        bar.setMaximumHeight(14)
        viewSpace.status.layout().addWidget(bar, 1)
        bar.hide()
        viewSpace.viewChanged.connect(self.viewChanged)
        app.jobStarted.connect(self.jobStarted)
        app.jobFinished.connect(self.jobFinished)
        
    def viewChanged(self, view):
        self.showProgress(view.document())
    
    def showProgress(self, document):
        job = jobmanager.job(document)
        if job and job.isRunning():
            buildtime = metainfo.info(document).buildtime
            if not buildtime:
                buildtime = 3.0 + document.blockCount() / 20 # very arbitrary estimate...
            self._bar.start(buildtime, job.elapsed())
        else:
            self._bar.stop(False)
    
    def jobStarted(self, document):
        if document == self.viewSpace().document():
            self.showProgress(document)
    
    def jobFinished(self, document, job, success):
        if document == self.viewSpace().document():
            self._bar.stop(success)
            if success:
                metainfo.info(document).buildtime = job.elapsed()


app.viewSpaceCreated.connect(ProgressBar.instance)
