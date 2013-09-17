"""semver.py
@OffbyOne Studios 2013
Class object for manipulating Semantic Versions
"""

class SemanticVersion(object):
    """A Semantic Version object for a plugin, as defined by version 2.0.0 on semver.org :
        http://semver.org/spec/v2.0.0.html
	
	Args:
		major: The major version number. (*1*.0.0)
		minor: The minor version number. (1.*0*.0)
		patch: The patch number (1.0.*0*)
		prerelease: The prerelease number, if applicable (1.0.0*+40*)
		metadata: Any relevant metadata to the version number.
	"""

    def __init__(self, major , minor, patch, prerelease = None, metadata = None):
        """Initializes a SemVer object. Defaults to version number 0.0.0 if no information is provided."""
        self.major = major
        self.minor = minor
        self.patch = patch
        self.prerelease = prerelease
        self.metadata = metadata

    class SemanticVersionParseError(Exception):
		pass

    @classmethod
    def parse(cls, string):
        """Parses a string to return its SemVer object.
			
		Args:
			string: A string representation of the SemVer object.
			
		Returns:
			A SemanticVersion object.
		"""
        if string is None:
            return None
        elif isinstance(string, cls):
            return string
        elif not isinstance(string, str):
            raise TypeError("Provided input is not a string")

        optargs = {}

        # Extract the metadata
        data = string.split('+')

        if len(data) > 2:
            raise cls.SemanticVersionParseError("Incorrect formatting of metadata")
        elif len(data) == 2:
            if '-' in data[1]:
                raise cls.SemanticVersionParseError("Incorrect formatting of metadata, metadata contains a hyphen")
            optargs["metadata"] = data[1]

        # Extract the prerelease
        data = data[0].split('-')

        if len(data) > 2:
            raise cls.SemanticVersionParseError("Incorrect formatting of prerelease")
        elif len(data) == 2:
            optargs["prerelease"] = data[1]

        # Extract the version data
        data = data[0].split('.')

        if len(data) != 3:
            raise cls.SemanticVersionParseError("Incorrect formatting of version numbers: {}".format(data))

        return cls(*data,**optargs)

    def __hash__(self):
        return hash((self.major, self.minor, self.patch, self.prerelease))

    # Comparison Operators

    def same_version_numbers(self, other):
        """Ignoring the prerelease version, returns true if the two SemVer objects have the same
            version numbers."""
        if self.major == other.major and \
           self.minor == other.minor and \
           self.patch == other.patch:
            return True
        else:
            return False


    def __eq__(self, other):
        """Compares two SemVer objects for equality, returns true if equal and false otherwise."""
        if self.same_version_numbers(other) and \
           self.prerelease == other.prerelease:
            return True
        else:
            return False


    def __ne__(self, other):
        """Compares two SemVer objects for equality, returns true if not equal and false otherwise."""
        return not (self == other)


    def __lt__(self, other):
        """Compares two SemVer objects for equality, returns true if the left hand object is less
            than the right hand object and false otherwise."""
        if self.major <= other.major and \
           self.minor <= other.minor and \
           self.patch <= other.patch:
            if not self.same_version_numbers(other):
                return True
            else:
                if not self.prerelease and not other.prerelease:
                    return False
                elif self.prerelease and other.prerelease:
                    return self.prerelease < other.prerelease
                elif self.prerelease:
                    return True

        return False


    def __gt__(self, other):
        """Compares two SemVer objects for equality, returns true if the left hand object is greater
            than the right hand object and false otherwise."""
        if self.major >= other.major and \
           self.minor >= other.minor and \
           self.patch >= other.patch:
            if not self.same_version_numbers(other):
                return True
            else:
                if not self.prerelease and not other.prerelease:
                    return False
                elif self.prerelease and other.prerelease:
                    return self.prerelease > other.prerelease
                elif self.prerelease:
                    return False
                else:
                    return True

        return False


    def __le__(self, other):
        """Compares two SemVer objects for equality, returns true if the left hand object is less
            than or equal to the right hand object and false otherwise."""
        return not (self > other)


    def __ge__(self, other):
        """Compares two SemVer objects for equality, return true if the left hand object is greater
            than or equal to the right hand object and false otherwise."""
        return not (self < other)

    # String Represenation

    def __str__(self):
        """Returns the human-readable string representation of a SemVer object."""
        return "{}.{}.{}{}{}".format(
            self.major,
            self.minor,
            self.patch,
            "-{}".format(self.prerelease) if not (self.prerelease is None) else "",
            "+{}".format(self.metadata) if not (self.metadata is None) else "",
        )

    def __repr__(self):
        """Returns the machine-readable string representation of a SemVer object."""
        return "SemanticVersion({}, {}, {}{}{})".format(
            self.major,
            self.minor,
            self.patch,
            ", prerelease={}".format(self.prerelease) if not (self.prerelease is None) else "",
            ", metadata={}".format(self.metadata) if not (self.metadata is None) else "",
        )

"""
#Example usage of Semantic Versioning

semver = SemanticVersion(1,0,0)
semver2 = SemanticVersion.parse("1.0.0+42")

if same_version_number(semver, semver2):
	pass
	
if semver >= semver2:
	pass
	
print semver

semstr = str(semver)
"""