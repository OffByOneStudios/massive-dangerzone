"""semver.py
@OffbyOne Studios 2013
Class object for manipulating Semantic Versions"""


class SemVer(object):
    """A Semantic Version object for a plugin, as defined by version 2.0.0 on semver.org :
        http://semver.org/spec/v2.0.0.html"""

    def __init__(self, major , minor, patch, prerelease = None, metadata = None):
        """Initializes a SemVer object. Defaults to version number 0.0.0 if no information is provided."""
        self.major = major
        self.minor = minor
        self.patch = patch
        self.prerelease = prerelease
        self.metadata = metadata


    @classmethod
    def parse(cls, string):
        """Parses a string to return its SemVer object."""
        if not isinstance(string, str):
            raise TypeError("Provided input is not a string")

        optargs = {}

        # Extract the metadata
        data = string.split('+')

        if len(data) > 2:
            raise ValueError("Incorrect formatting of metadata")
        elif len(data) == 2:
            if '-' in data[1]:
                raise ValueError("Incorrect formatting of metadata, metadata contains a hyphen")
            optargs["metadata"] = data[1]

        # Extract the prerelease
        data = data[0].split('-')

        if len(data) > 2:
            raise ValueError("Incorrect formatting of prerelease")
        elif len(data) == 2:
            optargs["prerelease"] = data[1]

        # Extract the version data
        data = data[0].split('.')

        if len(data) != 3:
            raise ValueError("Incorrect formatting of version numbers")

        return SemVer(data[0],data[1],data[2],**optargs)


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
        if self.major == other.major and \
           self.minor == other.minor and \
           self.patch == other.patch and \
           self.prerelease == other.prerelease:
            return True
        else:
            return False


    def __ne__(self, other):
        """Compares two SemVer objects for equality, returns true if not equal and false otherwise."""
        return not self == other


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
        return not self > other


    def __ge__(self, other):
        """Compares two SemVer objects for equality, return true if the left hand object is greater
            than or equal to the right hand object and false otherwise."""
        return not self < other


    # String Represenation

    def __str__(self):
        """Returns the human-readable string representation of a SemVer object."""
        if not self.prerelease and not self.metadata:
            return str(self.major) + "." + str(self.minor) + "." + str(self.patch)
        elif self.prerelease and self.metadata:
            return str(self.major) + "." + str(self.minor) + "." + str(self.patch) + "-" + str(self.prerelease) + "+" + str(self.metadata)
        elif self.prerelease:
            return str(self.major) + "." + str(self.minor) + "." + str(self.patch) + "-" + str(self.prerelease)
        elif self.metadata:
            return str(self.major) + "." + str(self.minor) + "." + str(self.patch) + "+" + str(self.metadata)


    def __repr__(self):
        """Returns the machine-readable string representation of a SemVer object."""
        if not self.prerelease and not self.metadata:
            return "SemVer(" + str(self.major) + ", " + str(self.minor) + ", " + str(self.patch) + ")"
        elif self.prerelease and self.metadata:
            return "SemVer(" + str(self.major) + ", "  + str(self.minor) + ", " + str(self.patch) + ", prerelease=" + str(self.prerelease) + ", metadata=" + str(self.metadata) + ")"
        elif self.prerelease:
            return "SemVer(" + str(self.major) + ", "  + str(self.minor) + ", " + str(self.patch) + ", prerelease=" + str(self.prerelease) + ")"
        elif self.metadata:
            return "SemVer(" + str(self.major) + ", "  + str(self.minor) + ", " + str(self.patch) + ", metadata=" + str(self.metadata) + ")"

