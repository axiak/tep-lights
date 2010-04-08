/**
@cond IGNORE

======================================================
 SFSEXP: Small, Fast S-Expression Library version 1.2
 Written by Matthew Sottile (matt@cs.uoregon.edu)
======================================================

Copyright (2003-2006). The Regents of the University of California. This
material was produced under U.S. Government contract W-7405-ENG-36 for Los
Alamos National Laboratory, which is operated by the University of
California for the U.S. Department of Energy. The U.S. Government has rights
to use, reproduce, and distribute this software. NEITHER THE GOVERNMENT NOR
THE UNIVERSITY MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR ASSUMES ANY
LIABILITY FOR THE USE OF THIS SOFTWARE. If software is modified to produce
derivative works, such modified software should be clearly marked, so as not
to confuse it with the version available from LANL.

Additionally, this library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation; either version 2.1 of the
License, or (at your option) any later version.

This library is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
for more details.

You should have received a copy of the GNU Lesser General Public License
along with this library; if not, write to the Free Software Foundation,
Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, U SA

LA-CC-04-094

@endcond
**/
/**
 * \defgroup viz Visualization and debugging routines
 */

/**
 * \file sexp_vis.h
 *
 * \brief API for emitting graphviz data structure visualizations.
 */
#ifndef __SEXP_VIS_H__
#define __SEXP_VIS_H__

/**
 * \ingroup viz
 *
 * Given a s-expression and a filename, this routine creates a DOT-file that
 * can be used to generate a visualization of the s-expression data structure.
 * This is useful for debugging to ensure that the structure is correct and
 * follows what was expected by the programmer.  Non-trivial s-expressions
 * can yield very large visualizations though.  Sometimes it is more
 * practical to visualize a portion of the structure if one knows where a bug
 * is likely to occur.
 *
 * \param sx     S-expression data structure to create a DOT file based on.
 * \param fname  Filename of the DOT file to emit.
 */
sexp_errcode_t sexp_to_dotfile(const sexp_t *sx, const char *fname);

#endif /* __SEXP_VIS_H__ */
