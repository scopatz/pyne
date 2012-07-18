#!/usr/bin/env python

"""
Module for parsing MCNP output data. MCNP is a general-purpose Monte Carlo
N-Particle code developed at Los Alamos National Laboratory that can be used for
neutron, photon, electron, or coupled neutron/photon/electron transport. Further
information on MCNP can be obtained from http://mcnp-green.lanl.gov/

Mctal and Runtpe classes still need work. Also should add Meshtal and Outp
classes.

"""

import collections
import struct
import math 
import os

from binaryreader import _BinaryReader, _FortranRecord

class Inp(object):
    """This class manages the creation of a plaintext MCNPX input file. The
    class manages the creation of cards (cell, surface, data, etc.) and handles
    the numbering of such cards. The class has also has a method to run the
    input script.

    The class is used by initializing the Inp object with various metadata
    settings that are printed as comments at the top of the input file. To
    actually define the simulation, the user makes calls (mostly in any order)
    to the appropriate _add_* methods. For example, there is a _add_cell()
    method that requires inputs of surface numbers, materials, etc. Calling an
    _add_* function does not cause anything to be written to the input file.
    Rather, this step is done by calling write(). The _add_* methods simply
    cause the creation of an instance of a mcnpcard, which is then saved to one
    of a number of ordered dictionaries in this class. write() then uses these
    ordered dictionaries to print the informaiton contained in them.

    Similar to input to Serpent, this class attempts to rely on "keywords",
    rather than just numbers, to relate cell cards to surface and material
    cards. This means that all surfaces and materials have string names, and a
    cell card is created by referring to these names.

    """

    def __init__(self, fname, title=None, description=None, author=None,
            modifications=None, path="", inpextension=".inp"):
        """
        This instantiates an Inp object, which initializes many of the fields
        in the class and creates the path directory if it does not already
        exist. None of the methods are actually called at this point (the input
        is still completely undefined).

        Parameters
        ----------
        fname : str
            Name of the input file.
        title : str
            The first (uncommented) line that is printed in the input file.
        description : str
            Text that is written to the input file as comments as a perhaps
            lengthy description of the simulation specified by the input file.
        author : str
            The name of the author of the input. This is printed at the top of
            the input file, below the description.
        modifications : tuple
            A tuple of strings that describe modifications to the input. A
            primitive version record. There are surely better ways to input
            this.
        path : str
            The path where the input file should be written.
        inpextension : str
            The filename extension for the input file.
        """

        self.inpextension = inpextension
        self.fname = fname
        if len(path) > 0 and path[-1] != os.sep:
            path += os.sep
        self.path = path + self.fname + os.sep
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        self.f = open(self.path + fname + inpextension, 'w')
        self.cells = collections.OrderedDict()
        self.surfaces = collections.OrderedDict()
        self.materials = collections.OrderedDict()
        self.scattering_laws = collections.OrderedDict()
        self.source = None
        self.source_points = None
        self.miscdata = []
        self.tallies = collections.OrderedDict()
        self.surfaceCard = 0
        self.cellCard = 0
        self.matCard = 0
        self.tally_cellflux_card = 4
        self.title = title
        self.description = description
        self.author = author
        self.modifications = modifications

    def _next_mat_card(self):
        self.matCard = self.matCard + 100

    def set_title(self, title):
        self.title = title

    def set_description(self, description):
        self.description

    def add_cell(self, name, matName, density, densityUnits, inSurfaceNames,
            outSurfaceNames, imp, temp=None, vol=None):
        # TODO only assign if no errors. check uniqueness of name
        # TODO clean up rror checking; make it consistent
        #try:
            self._unique("cell", name)

            if matName not in self.materials:
                raise Exception("Material " + matName + " does not exist," \
                        " cannot use in cell")

            inSurfaces = []
            # TODO initalize for efficiency
            for surfaceName in inSurfaceNames:
                if surfaceName not in self.surfaces:
                    raise Exception("Surface " + surfaceName + " does not " \
                            "exist, cannot use in cell")
                inSurfaces = inSurfaces + [self.surfaces[surfaceName]]

            outSurfaces = []
            for surfaceName in outSurfaceNames:
                if surfaceName not in self.surfaces:
                    raise Exception("Surface " + surfaceName + " does not " \
                            "exist, cannot use in cell")
                outSurfaces = outSurfaces + [self.surfaces[surfaceName]]

            self.cells[name] = mcnpcards.Cell(self._next_cell_card(), name,
                    self.materials[matName], density, densityUnits, inSurfaces,
                    outSurfaces, imp, temp, vol)
        #except:
        #    raise Exception("Failed to add a cell")

    def add_cell_void(self, name, inSurfaceNames, outSurfaceNames, imp):
        # TODO only assign if no errors. check uniqueness of name
        #try:
            self._unique("cell", name)

            inSurfaces = []
            # TODO initalize for efficiency
            for surfaceName in inSurfaceNames:
                if surfaceName not in self.surfaces:
                    raise Exception("Surface " + surfaceName + " does not " \
                            "exist, cannot use in cell")
                inSurfaces = inSurfaces + [self.surfaces[surfaceName]]

            outSurfaces = []
            for surfaceName in outSurfaceNames:
                if surfaceName not in self.surfaces:
                    raise Exception("Surface " + surfaceName + " does not " \
                            "exist, cannot use in cell")
                outSurfaces = outSurfaces + [self.surfaces[surfaceName]]

            self.cells[name] = mcnpcards.CellVoid(self._next_cell_card(), name,
                    inSurfaces, outSurfaces, imp)
        #except:
        #    raise Exception("Failed to add a cell")

    def add_surface_plane(self, name, dirstr, pos, 
                        reflecting=False, white=False):
        # TODO only assign if no errors. check uniqueness of name
        #try:
            self._unique("surface", name)
            self.surfaces[name] = mcnpcards.Plane(self._next_surface_card(),
                    name, dirstr, pos, reflecting, white)
        #except:
        #    raise Exception("Failed to add a plane surface.")


    def add_surface_cylinder(self, name, dirstr, radius,
                           reflecting=False, white=False):
        # TODO only assign if no errors. check uniqueness of name
        #try:
            self._unique("surface", name)
            self.surfaces[name] = mcnpcards.Cylinder(self._next_surface_card(),
                    name, dirstr, radius, reflecting, white)
        #except:
        #    raise Exception("Failed to add a cylinder surface.")

    def add_surface_originsphere(self, name, radius,
                                 reflecting=False, white=False):
        # TODO only assign if no errors, check uniqueness of name
        self._unique("surface", name)
        self.surfaces[name] = mcnpcards.Sphere(self._next_surface_card(),
                name, radius)

    def add_surface_rectangularparallelepiped(self, name, xmin, xmax,
                                              ymin, ymax, zmin, zmax,
                                              reflecting=False, white=False):
        self.surfaces[name] = mcnpcards.RectangularParallelepiped(
                self._next_surface_card(), name, xmin, xmax, ymin, ymax,
                zmin, zmax, reflecting, white)

    def add_material(self, name, comment, ZAIDs, densityUnits, densities,
            temp=None):
        # TODO only assign if no errors. check uniqueness of name
        #try:
            self._unique("material", name)
            self.materials[name] = mcnpcards.Material(self._next_mat_card(),
                    name, comment, ZAIDs, densityUnits, densities, temp)
        #except:
        #    raise Exception("Failed to add a material")

    def add_scattering_law(self, material_name, libraries, temp=None):
        # TODO simple version now: user simply supplies the library names.
        if material_name not in self.materials:
            raise Exception("Material {0} does not exist. Cannot create "
                "scattering law card for nonexistant materials.".format(
                    material_name))
        material_no = self.materials[material_name].card_no
        # Each material can only have one scattering law.
        self.scattering_laws[material_name] = mcnpcards.ScatteringLaw(
                material_no,
                libraries,
                temp)

    def add_criticality_source(self, n_histories=1000,
                               keff_guess=1.0,
                               n_skip_cycles=30,
                               n_cycles=130):
        # TODO there are other options
        self.source = mcnpcards.Criticality(n_histories, keff_guess,
                n_skip_cycles, n_cycles)

    def add_criticality_source_points(self, points=[[0,0,0]]):
        # TODO
        self.source_points = mcnpcards.CriticalitySourcePoints(points)

    def add_tally_cellflux(self, name, particle, cell_names):
        # Check to see that the relevant particle type is already in use.
        self._unique("tally", name)
        cell_nos = []
        for cell_name in cell_names:
            if cell_name not in self.cells:
                raise Exception("The cell {0} is not defined for this input "
                        "file.".format(cell_name))
            cell_nos += [self.cells[cell_name].card_no]
            self.tallies[name] = mcnpcards.TallyCellFlux(
                    self._next_tally_cell_flux_card(), name,
                    particle, cell_nos)

    def add_tally_multiplier(self, tally_name, multsets):
        """[(c, "matname", MTs), (c, "matname", MTs)
        TODO can tally_no be zero, like with the En card?
        ERROR check: the material used for multiplier is the same as the one
        used for the cell in the actual tally?
        TODO want to make the -1 input smarter
        """
        if tally_name not in self.tallies:
            raise Exception("The tally specified for this tally multiplier "
                    "card does not exist.")
        tally_no = self.tallies[tally_name].card_no
        newmultsets = []
        for multset in multsets:
            if len(multset) == 1:
                newmultsets += [multset]
            elif len(multset) == 3:
                mat_name = multset[1]
                if mat_name not in self.materials:
                    raise Exception("The material specified in this tally "
                            "multiplier card does not exist.")
                mat_no = self.materials[mat_name].card_no
                newmultsets += [(multset[0], mat_no, multset[2])]
        self.miscdata += [mcnpcards.TallyMultiplier(tally_no, newmultsets)]

    def add_tally_energy(self, tally_name, energies):
        # TODO allow for logarithmic input.
        if tally_name is 0:
            # If this energy card is supposed to apply to all energies.
            tally_no = 0
        else:
            if tally_name not in self.tallies:
                raise Exception("The tally specified for this tally energy "
                        "card does not exist.")
            tally_no = self.tallies[tally_name].card_no
        self.miscdata += [mcnpcards.TallyEnergy(tally_no, energies)]

    def add_printdump(self):
        self.miscdata += [mcnpcards.PrintDump()]

    def write(self):
        if self.title != None:
            self._write_card(self.title)
            self._write_comment("")
        if self.source is None:
            raise Exception("Input file does not have a particle source, "
                    "and must have one.")
        self._write_comment("******************** File Description "
                "******************************")
        self._write_comment("")
        if self.description != None:
            self._write_comment("Description: " + self.description)
        self._write_comment("")
        if self.author != None:
            self._write_comment("Author: " + self.author)
        self._write_comment("")
        self._write_modifications()
        self._write_comment("")
        # writing cells
        self._write_comment("")
        self._write_deck_header_line("Cell")
        self._write_comment("")
        for cellName in self.cells:
            self._write_card(self.cells[cellName].card())
        self._write_return()

        # writing surfaces
        self._write_comment("")
        self._write_deck_header_line("Surface")
        self._write_comment("")
        for surfaceName in self.surfaces:
            self._write_card(self.surfaces[surfaceName].card())
        self._write_return()

        # writing data cards
        self._write_comment("")
        self._write_deck_header_line("Data")
        # writing materials
        self._write_comment("")
        self._write_data_header_line("Materials")
        for materialName in self.materials:
            self._write_comment("")
            self._write_material_comment(self.materials[materialName].comment())
            self._write_comment("")
            self._write_material_card(self.materials[materialName].card())
            if materialName in self.scattering_laws:
                self._write_card(self.scattering_laws[materialName].card())

        # Writing source cards.
        # Want a way to know what type of source we're using.
        self._write_comment("")
        self._write_data_header_line("Source")
        self._write_comment("")
        self._write_card(self.source.card())
        if self.source_points is not None:
            self._write_card(self.source_points.card())

        # Writing tally cards.
        if len(self.tallies) > 0:
            # There are tally cards
            self._write_comment("")
            self._write_data_header_line("Tallies")
            self._write_comment("")
            for tally_name in self.tallies:
                self._write_card(self.tallies[tally_name].card())

        # Write miscellaneous data cards.
        for card in self.miscdata:
            self._write_card(card.card())
        self.f.close()

    def _write_modifications(self):
        first = True
        for modtuple in self.modifications:
            if first == True:
                self._write_comment("Modifications: " + modtuple[0] + " - " +
                        modtuple[1])
                first = False
            else:
                self._write_comment("               " + modtuple[0] + " - " +
                        modtuple[1])

    def _write_return(self):
        self.f.write("\n")

    def _write_card(self, string2print):
        '''Checks length of string, makes sure it's less than 80 characters.
            TODO skipping this operation based on the location of the $ needs
            to be improved.
        '''
        stringIsMultipleLines = False
        firstLine = True
        max_line_length = 74
        # If there is no comment on this line or it starts after the 74th
        # character.
        if ((string2print.find('$') < 0) or
                (string2print.find('$') > max_line_length)):
            while len(string2print) > max_line_length:
                stringIsMultipleLines = True
                spaceindex = string.rfind(string2print, ' ', 
                                          0, max_line_length) + 1
                if firstLine:
                    self.f.write(string2print[0:spaceindex] + "\n")
                    firstLine = False
                else:
                    self.f.write("     " + string2print[0:spaceindex] + "\n")
                string2print = string2print[spaceindex:len(string2print)]
            if stringIsMultipleLines and not firstLine:
                self.f.write(5 * " ")
        self.f.write(string2print + "\n")

    def _write_material_card(self, string2print):
        self.f.write(string2print)

    def _write_comment(self, string2print):
        '''
        '''
        if string2print == "":
            self.f.write("c\n")
            return
        while len(string2print) > 74:
            spaceindex = string.rfind(string2print, ' ', 0, 74) + 1
            self.f.write("c " + string2print[0:spaceindex] + "\n")
            string2print = string2print[spaceindex:len(string2print)]
        self.f.write("c " + string2print + "\n")

    def _write_material_comment(self, stringTuple):
        if type(stringTuple) is not tuple:
            raise Exception("Material comment input must be a tuple.")
        for string in stringTuple:
            self._write_comment("    -- " + string)

    def writeHeaderLine(self):
        self.f.write("C ==========================\n")

    def _write_deck_header_line(self, header):
        self._write_comment("*** " + header + " Cards ***")

    def _write_data_header_line(self, header):
        self._write_comment(" ----- " + header)

    def run(self, plot=False, outfname=None, mctafname=None):
        curdir = os.path.abspath(os.path.curdir)
        print curdir
        print self.path
        os.chdir(self.path)
        to_execute = "mcnpx i=%s%s" % (self.fname, self.inpextension)
        if outfname is not None:
            to_execute += " o=%s" % outfname
        if mctafname is not None:
            # Did we even run for an MCTA file?
            to_execute += " m=%s" % mctafname
        if plot:
            to_execute += " ip"
        os.system(to_execute)
        os.chdir(curdir)

    def clean(self, runt=True, src=True, out=False, mcta=False, com=True):
        """
        
        TODO not platform independent; os.remove() does not take reg exps.
        """

        curdir = os.path.abspath(os.path.curdir)
        os.chdir(self.path)
        if runt:
            os.system("rm *runt*")
        if src:
            os.system("rm *srct*")
        if out:
            os.system("rm *out*")
        if mcta:
            os.system("rm *mcta*")
        if com:
            os.system("rm *com*")
        os.chdir(curdir)

    def _unique(self, card_type, name):
        if card_type == "cell":
            dict_to_check = self.cells
        elif card_type == "surface":
            dict_to_check = self.surfaces
        elif card_type == "material":
            dict_to_check = self.materials
        elif card_type == "tally":
            dict_to_check = self.tallies
        else:
            raise Exception("TODO")
        if name in dict_to_check:
            raise Exception("This %s name has already been used for "
                    "another %s" % (card_type, card_type))
        return

    def _next_surface_card(self):
        self.surfaceCard += 1
        return self.surfaceCard

    def _next_cell_card(self):
        self.cellCard += 1
        return self.cellCard

    def _next_mat_card(self):
        self.matCard += 1
        return self.matCard

    def _next_tally_cell_flux_card(self):
        self.tally_cellflux_card += 10
        return self.tally_cellflux_card


class Mctal(object):
    def __init__(self):
        pass

    def read(self, filename):
        """
        Parses a 'mctal' tally output file from MCNP. Currently this
        only supports reading the kcode data- the remaining tally data
        will not be read.
        """

        # open file
        self.f = open(filename, 'r')

        # get code name, version, date/time, etc
        words = self.f.readline().split()
        self.codeName = words[0]
        self.codeVersion = words[1]
        self.codeDate = words[2]
        self.codeTime = words[3]
        self.n_dump = words[4]
        self.n_histories = int(words[5])
        self.n_prn       = int(words[6])

        # comment line of input file
        self.comment = self.f.readline().strip()

        # read tally line
        words = self.f.readline().split()
        self.n_tallies = words[1]
        if len(words) > 2:
            # perturbation tallies present
            pass

        # read tally numbers
        tally_nums = [int(i) for i in self.f.readline().split()]

        # read tallies
        for i_tal in tally_nums:
            pass

        # read kcode information
        words = self.f.readline().split()
        self.n_cycles = int(words[1])
        self.n_inactive = int(words[2])
        vars_per_cycle = int(words[3])

        self.k_col = []
        self.k_abs = []
        self.k_path = []
        self.prompt_life_col = []
        self.prompt_life_path = []
        self.avg_k_col = []
        self.avg_k_abs = []
        self.avg_k_path = []
        self.avg_k_combined = []
        self.avg_k_combined_active = []
        self.prompt_life_combined = []
        self.cycle_histories = []
        self.avg_k_combined_FOM = []

        for cycle in range(self.n_cycles):
            # read keff and prompt neutron lifetimes
            if vars_per_cycle == 0 or vars_per_cycle == 5:
                values = [float(i) for i in get_words(self.f, lines = 1)]
            elif vars_per_cycle == 19:
                values = [float(i) for i in get_words(self.f, lines = 4)]
            
            self.k_col.append(values[0])
            self.k_abs.append(values[1])
            self.k_path.append(values[2])
            self.prompt_life_col.append(values[3])
            self.prompt_life_path.append(values[4])

            if vars_per_cycle <= 5:
                continue

            avg, stdev = (values[5],values[6])
            self.avg_k_col.append((avg,stdev))
            avg, stdev = (values[7],values[8])
            self.avg_k_abs.append((avg,stdev))
            avg, stdev = (values[9],values[10])
            self.avg_k_path.append((avg,stdev))
            avg, stdev = (values[11],values[12])
            self.avg_k_combined.append((avg,stdev))
            avg, stdev = (values[13],values[14])
            self.avg_k_combined_active.append((avg,stdev))
            avg, stdev = (values[15],values[16])
            self.prompt_life_combined.append((avg,stdev))
            self.cycle_histories.append(values[17])
            self.avg_k_combined_FOM.append(values[18])
            
def get_words(f, lines = 1):
    words = []
    for i in range(lines):
        local_words = f.readline().split()
        words += local_words
    return words

class SourceSurf(object):
    def __init__(self):
        pass

class TrackData(object):
    def __init__(self):
        pass

class SurfSrc(_BinaryReader):

    def __init__(self, filename, mode="rb"):
        super(SurfSrc, self).__init__(filename,mode)

    def __str__(self):
        return self.print_header()

    def print_header(self):
        headerString  = "Code: {0} (version: {1}) [{2}]\n".format(self.kod, self.ver, self.loddat)
        headerString += "Problem info: ({0}) {1}\n{2}\n".format(self.idtm, self.probid, self.aid)
        headerString += "Showing dump #{0}\n".format(self.knod)
        headerString += "{0} histories, {1} tracks, {2} record size, {3} surfaces, {4} histories\n".format(self.np1, self.nrss, self.ncrd, self.njsw, self.niss)
        headerString += "{0} cells, source particle: {1}, macrobody facet flag: {2}\n".format(self.niwr, self.mipts, self.kjaq)
        for i in self.surflist:
            headerString += "Surface {0}: facet {1}, type {2} with {3} parameters: (".format(i.id, i.facetId, i.type, i.numParams)
            if i.numParams > 1:
                for j in i.surfParams:
                    headerString += " {0}".format(j)
            else:
                headerString += " {0}".format(i.surfParams)
            headerString += ")\n"
        headerString += "Summary Table: " + str(self.summaryTable)

        return headerString

    def print_tracklist(self):
        trackData = "Track Data\n"
  #                       1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890
        trackData +=     "       nps   BITARRAY        WGT        ERG        TME             X             Y             Z          U          V     COSINE  |       W\n"
        for j in self.tracklist:
            trackData += "%10d %10g %10.5g %10.5g %10.5g %13.5e %13.5e %13.5e %10.5f %10.5f %10.5f  | %10.5f " % (j.nps, j.bitarray, j.wgt, j.erg, j.tme, j.x, j.y, j.z, j.u, j.v, j.cs, j.w) + "\n"

        return trackData

    def compare(self,other):
        """ """

        if other.kod != self.kod:
            print "kod does not match"
            return False
        if other.ver != self.ver:
            print "ver does not match"
            return False
        if other.loddat != self.loddat:
            print "loddat does not match"
            return False

        if other.ncrd != self.ncrd:
            print "ncrd does not match"
            return False
        if other.njsw != self.njsw:
            print "njsw does not match"
            return False

        if other.niwr  != self.niwr:
            print "niwr does not match"
            return False
        if other.mipts != self.mipts:
            print "mipts does not match"
            return False
        if other.kjaq  != self.kjaq:
            print "kjaq does not match"
            return False

        for surf in range(len(self.surflist)):
            if other.surflist[surf].id         != self.surflist[surf].id:
                print "surf " + str(surf) + " ID doesn't match"
                return False
            if other.surflist[surf].facetId    != self.surflist[surf].facetId:
                print "surf " + str(surf) + " facetId doesn't match"
                return False
            if other.surflist[surf].type       != self.surflist[surf].type:
                print "surf " + str(surf) + " type doesn't match"
                return False
            if other.surflist[surf].numParams  != self.surflist[surf].numParams:
                print "surf " + str(surf) + " numParams doesn't match"
                return False
            if other.surflist[surf].surfParams != self.surflist[surf].surfParams:
                print "surf " + str(surf) + " surfParams doesn't match"
                return False

        return True

    def read_header(self):
        """Read in the header block data

        This block comprises 4 fortran records which we refer to as:
        header, table1, table2, summary
        """
        # read header record
        header = self.get_fortran_record()

        # interpret header 
        self.kod    = header.get_string(8)[0]  # code identifier
        self.ver    = header.get_string(5)[0]  # code version identifier
        self.loddat = header.get_string(8)[0]  # code version date
        self.idtm   = header.get_string(19)[0] # current date and time
        self.probid = header.get_string(19)[0] # problem identification string
        self.aid    = header.get_string(80)[0] # title card of initial run
        self.knod   = header.get_int()[0]      # dump number

        # read table 1 record; various counts and sizes
        tablelengths = self.get_fortran_record()

        # interpret table lengths
        self.np1  = tablelengths.get_long()[0]  # number of histories used to generate source
        self.nrss = tablelengths.get_long()[0]  # number of tracks written to surface source
        self.ncrd = tablelengths.get_int()[0]  # number of values in surface source record
                                               # 6 for a spherical source
                                               # 11 otherwise
        self.njsw = tablelengths.get_int()[0]   # number of surfaces
        self.niss = tablelengths.get_long()[0]  # number of histories written to surface source

        if self.np1 < 0:
            # read table 2 record; more size info
            tablelengths = self.get_fortran_record()

            self.niwr  = tablelengths.get_int()[0]  # number of cells in surface source card
            self.mipts = tablelengths.get_int()[0]  # source particle type
            self.kjaq  = tablelengths.get_int()[0]  # macrobody facet flag
            self.table2extra=[]
            while tablelengths.numBytes > tablelengths.pos:
                self.table2extra += tablelengths.get_int()
            # print "np1 is ", self.np1
        else:
            # print "np1 is ", self.np1
            pass
        
        self.orignp1 = self.np1
        print self.np1
        self.np1 = abs(self.np1)

        # get info for each surface
        self.surflist = []
        for j in range(self.njsw):
            # read next surface info record
            self.surfaceinfo = self.get_fortran_record()
            
            surfinfo = SourceSurf()
            surfinfo.id = self.surfaceinfo.get_int()            # surface ID
            if self.kjaq == 1:
                surfinfo.facetId = self.surfaceinfo.get_int()   # facet ID
            else:
                surfinfo.facetId = -1                           # dummy facet ID

            surfinfo.type = self.surfaceinfo.get_int()                 # surface type
            surfinfo.numParams = self.surfaceinfo.get_int()[0]         # number of surface parameters
            surfinfo.surfParams = self.surfaceinfo.get_double(surfinfo.numParams)

            self.surflist.append(surfinfo)                  

        # We read any extra records as determined by njsw+niwr...
        #  No known case of their actual utility is known currently
        for j in range(self.njsw,self.njsw+self.niwr):
            self.get_fortran_record()
            print "Extra info in header not handled:", j

        # read summary table record
        summaryInfo = self.get_fortran_record()
        self.summaryTable = summaryInfo.get_int((2+4*self.mipts)*(self.njsw+self.niwr)+1)
        self.summaryExtra=[]
        while summaryInfo.numBytes > summaryInfo.pos:
            self.summaryExtra += summaryInfo.get_int()
        

    def read_tracklist(self):
        """
        Reads in track records for individual particles.
        """
        self.tracklist = []
        for j in range(self.nrss):
            trackInfo = self.get_fortran_record()
            trackData = TrackData()
            trackData.record   = trackInfo.get_double(self.ncrd)
            trackData.nps      = trackData.record[0]
            trackData.bitarray = trackData.record[1]
            trackData.wgt      = trackData.record[2]
            trackData.erg      = trackData.record[3]
            trackData.tme      = trackData.record[4]
            trackData.x        = trackData.record[5]
            trackData.y        = trackData.record[6]
            trackData.z        = trackData.record[7]
            trackData.u        = trackData.record[8]
            trackData.v        = trackData.record[9]
            trackData.cs       = trackData.record[10]
            trackData.w        = math.copysign(math.sqrt(1 - trackData.u*trackData.u - trackData.v*trackData.v),trackData.bitarray)
            # trackData.bitarray = abs(trackData.bitarray)
            
            self.tracklist.append(trackData)       
        return


    def put_header(self):
        """
        Write the header part of the header
        to the surface source file
        """
        rec = [self.kod, self.ver, self.loddat, self.idtm, self.probid, self.aid]
        newrecord = _FortranRecord("".join(rec), len("".join(rec)))
        newrecord.put_int([self.knod])
        self.put_fortran_record(newrecord)
        return
    
    
    def put_table_1(self):
        """
        Write the table1 part of the header
        to the surface source file
        """
        newrecord = _FortranRecord("", 0)
        newrecord.put_long( [self.np1])
        newrecord.put_long( [self.nrss])
        newrecord.put_int(  [self.ncrd])
        newrecord.put_int(  [self.njsw])
        newrecord.put_long( [self.niss])
        self.put_fortran_record(newrecord)
        return
    
    
    def put_table_2(self):
        """
        Write the table2 part of the header
        to the surface source file
        """
        newrecord = _FortranRecord("", 0)
        newrecord.put_int( [self.niwr ])
        newrecord.put_int( [self.mipts])
        newrecord.put_int( [self.kjaq ])
        newrecord.put_int( self.table2extra)
        self.put_fortran_record(newrecord)
        return


    def put_surface_info(self):
        """
        Write the record for each surface
        to the surface source file
        """

        for cnt, s in enumerate(self.surflist):
            newrecord = _FortranRecord("",0)
            newrecord.put_int(s.id)
            if self.kjaq == 1:
                newrecord.put_int(s.facetId) # don't add a 'dummy facet ID'
            # else no macrobody flag byte in the record

            newrecord.put_int(s.type)
            newrecord.put_int(s.numParams)
            newrecord.put_double(s.surfParams)
            
            self.put_fortran_record(newrecord)
        return
        
        
    def put_summary(self):
        """
        Write the summary part of the header
        to the surface source file
        """
        newrecord = _FortranRecord("", 0)
        newrecord.put_int( list(self.summaryTable) )
        newrecord.put_int( list(self.summaryExtra) )
        #newrecord.put_int( [self.summaryTable])
        #newrecord.put_int( [self.summaryExtra])
        self.put_fortran_record(newrecord)
        return


class Srctp(_BinaryReader):
    """This class stores source site data from a 'srctp' file written by
    MCNP. The source sites are stored in the 'fso' array in MCNP.
    """

    def __init__(self, filename):
        super(Srctp, self).__init__(filename)

    def read(self):
        # read header block
        header = self.get_fortran_record()

        # interpret header block
        k = header.get_int() # unique code (947830)
        self.loc_next = header.get_int() # location of next site in FSO array (ixak)
        self.n_run = header.get_int() # source particles yet to be run (nsa)
        self.loc_store = header.get_int() # where to store next source neutron (ist)
        self.n_source = header.get_int() # number of source points in fso (mrl)

        # read source site array
        fso = self.get_fortran_record()
        
        self.sites = []
        for i in range(self.n_source):
            vals = fso.get_double(11)

            site = SourceSite()
            site.x = vals[0]
            site.y = vals[1]
            site.z = vals[2]
            site.E = vals[3]

            self.sites.append(site)

    def remainingSites(self):
        index = self.loc_next - 1
        if (self.loc_next + self.n_run) >= self.n_source:
            return (self.sites[index:] + 
                    self.sites[:self.n_run - (self.n_source - index)])
        else:
            return self.sites[index : index + self.n_run]

    def __repr__(self):
        return "<Srctp: {0}>".format(self.f.name)


class SourceSite(object):
    
    def __init__(self):
        pass

    def __repr__(self):
        return "<SourceSite: ({0.x},{0.y},{0.z})>".format(self)


class Runtpe(_BinaryReader):

    def __init__(self, filename):
        super(Runtpe, self).__init__(filename)

    def read(self, filename):
        # read identification block
        header = self.get_fortran_record()

        # parse identification block
        self.codeName = header.get_string(8)
        self.codeVersion = header.get_string(5)
        self.codeDate = header.get_string(8)
        header.get_string(19) # machine designator, date and time
        self.chargeCode = header.get_string(10)
        self.problemID = header.get_string(19)
        self.problemIDsurf = header.get_string(19)
        self.title = header.get_string(80)
        header.pos += 3*6*11 # skip user file characteristics
        self.n_tables = header.get_int()

        # read cross-section tables
        self.tables = []
        for i in range(self.n_tables):
            self.tables.append(self.get_fortran_record())
            

    def __repr__(self):
        return "<Runtpe: {0}>".format(self.f.name)


class Xsdir(object):

    def __init__(self, filename):
        self.f = open(filename, 'r')
        self.filename = os.path.abspath(filename)
        self.directory = os.path.dirname(filename)
        self.awr = {}
        self.tables = []

        self.read()

    def read(self):
        # Go to beginning of file
        self.f.seek(0)

        # Read first section (DATAPATH)
        line = self.f.readline()
        words = line.split()
        if words:
            if words[0].lower().startswith('datapath'):
                index = line.index('=')
                self.datapath = line[index+1:].strip()

        # Read second section
        line = self.f.readline()
        words = line.split()
        assert len(words) == 3
        assert words[0].lower() == 'atomic'
        assert words[1].lower() == 'weight'
        assert words[2].lower() == 'ratios'

        while True:
            line = self.f.readline()
            words = line.split()

            # Check for end of second section
            if len(words) % 2 != 0 or words[0] == 'directory':
                break
            
            for zaid, awr in zip(words[::2], words[1::2]):
                self.awr[zaid] = awr

        # Read third section
        while words[0] != 'directory':
            words = self.f.readline().split()
            
        while True:
            words = self.f.readline().split()
            if not words:
                break

            # Handle continuation lines
            while words[-1] == '+':
                extraWords = self.f.readline().split()
                words = words + extraWords
            assert len(words) >= 7

            # Create XsdirTable object and add to line
            table = XsdirTable()
            self.tables.append(table)
            
            # All tables have at least 7 attributes
            table.name = words[0]
            table.awr = float(words[1])
            table.filename = words[2]
            table.access = words[3]
            table.filetype = int(words[4])
            table.address = int(words[5])
            table.tablelength = int(words[6])

            if len(words) > 7:
                table.recordlength = int(words[7])
            if len(words) > 8:
                table.entries = int(words[8])
            if len(words) > 9:
                table.temperature = float(words[9])
            if len(words) > 10:
                table.ptable = (words[10] == 'ptable')

    def find_table(self, name):
        tables = []
        for table in self:
            if name in table.name:
                tables.append(table)
        return tables

    def to_xsdata(self, filename):
        xsdata = open(filename, 'w')
        for table in self.tables:
            if table.serpent_type == 1:
                xsdata.write(table.to_serpent() + '\n')
        xsdata.close()

    def __iter__(self):
        for table in self.tables:
            yield table

class XsdirTable(object):

    def __init__(self):
        self.name = None
        self.awr = None
        self.filename = None
        self.access = None
        self.filetype = None
        self.address = None
        self.tablelength = None
        self.recordlength = None
        self.entries = None
        self.temperature = None
        self.ptable = False

    @property
    def alias(self):
        return self.name

    @property
    def serpent_type(self):
        if self.name.endswith('c'):
            return 1
        elif self.name.endswith('y'):
            return 2
        elif self.name.endswith('t'):
            return 3
        else:
            return None

    @property
    def metastable(self):
        # Only valid for neutron cross-sections
        if not self.name.endswith('c'):
            return

        # Handle special case of Am-242 and Am-242m
        if self.zaid == '95242':
            return 1
        elif self.zaid == '95642':
            return 0

        # All other cases
        A = int(self.zaid) % 1000
        if A > 600:
            return 1
        else:
            return 0

    @property
    def zaid(self):
        return self.name[:self.name.find('.')]

    def to_serpent(self, directory=''):
        # Adjust directory
        if directory:
            if not directory.endswith('/'):
                directory = directory.strip() + '/'

        return "{0} {0} {1} {2} {3} {4} {5} {6} {7}".format(
            self.name, self.serpent_type, self.zaid, 1 if self.metastable else 0,
            self.awr, self.temperature/8.6173423e-11, self.filetype - 1,
            directory + self.filename)

    def __repr__(self):
        return "<XsDirTable: {0}>".format(self.name)
