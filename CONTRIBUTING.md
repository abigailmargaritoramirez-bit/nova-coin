# Contributing to NOVA COIN

Thank you for considering contributing to NOVA COIN! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful, inclusive, and professional. We're building a community-driven project.

## Getting Started

### Prerequisites
- Node.js >= 16.0
- npm or yarn
- Git
- Basic knowledge of Solidity and JavaScript

### Local Setup

```bash
# Clone the repository
git clone https://github.com/abigailmargaritoramirez-bit/nova-coin.git
cd nova-coin

# Install dependencies
npm install

# Compile contracts
npm run compile

# Run tests
npm test
```

## Development Workflow

### 1. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Changes
- Write clean, commented code
- Follow Solidity best practices
- Add tests for new functionality
- Update documentation as needed

### 3. Test Your Changes
```bash
# Run all tests
npm test

# Run specific test file
npm test test/NovaCoin.test.js

# Check gas usage
npm run gas-report

# Code coverage
npm run coverage
```

### 4. Commit Your Changes
```bash
git add .
git commit -m "feat: describe your changes"
```

**Commit Message Format:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Tests
- `refactor:` Code refactoring
- `style:` Code style
- `chore:` Build or dependency updates

### 5. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```

Then open a Pull Request on GitHub with:
- Clear description of changes
- Reference to related issues
- Screenshots or gas reports if applicable

## Coding Standards

### Solidity
- Use Solidity 0.8.0 or higher
- Follow OpenZeppelin conventions
- Include NatSpec documentation
- Keep functions focused and readable
- Add access control where needed

**Example:**
```solidity
/**
 * @dev Transfer tokens to recipient
 * @param recipient Address to receive tokens
 * @param amount Amount of tokens to transfer
 * @return Boolean indicating success
 */
function transfer(address recipient, uint256 amount) 
    public 
    override 
    returns (bool) 
{
    require(recipient != address(0), "Invalid recipient");
    // Implementation
}
```

### JavaScript/TypeScript
- Use 2-space indentation
- Use camelCase for variables/functions
- Use PascalCase for classes/contracts
- Write descriptive variable names
- Add comments for complex logic

### Documentation
- Update README for new features
- Document deployment procedures
- Add examples for new functions
- Keep changelog updated

## Security Considerations

### Before Submitting
- [ ] Run security audit locally
- [ ] Check for reentrancy issues
- [ ] Verify access controls
- [ ] Test edge cases
- [ ] Check gas optimization

### Security Issues
If you find a security vulnerability:
1. **DO NOT** open a public issue
2. Email: security@novacoin.dev
3. Include detailed description
4. Wait for response before disclosure

## Testing Requirements

### New Features Must Include
- Unit tests
- Integration tests
- Edge case testing
- Error handling tests

### Test Template
```javascript
describe("NovaCoin", function () {
  let novaCoin;
  let owner, addr1, addr2;

  beforeEach(async function () {
    [owner, addr1, addr2] = await ethers.getSigners();
    const NovaCoin = await ethers.getContractFactory("NovaCoin");
    novaCoin = await NovaCoin.deploy(1000000);
  });

  describe("Transfer", function () {
    it("Should transfer tokens", async function () {
      await novaCoin.transfer(addr1.address, 100);
      const balance = await novaCoin.balanceOf(addr1.address);
      expect(balance).to.equal(100);
    });

    it("Should fail with insufficient balance", async function () {
      await expect(
        novaCoin.connect(addr1).transfer(owner.address, 1000)
      ).to.be.revertedWith("Insufficient balance");
    });
  });
});
```

## Pull Request Process

1. **Update tests** - Add tests for new code
2. **Run tests** - Ensure all tests pass
3. **Update docs** - Update README/docs if needed
4. **Describe changes** - Clear PR description
5. **Request review** - Ask maintainers to review
6. **Address feedback** - Make requested changes
7. **Merge** - Approved PR gets merged

## Reporting Issues

### Bug Report Template
```markdown
## Description
Clear description of the bug

## Steps to Reproduce
1. Step one
2. Step two
3. ...

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- Node version: 
- npm version:
- OS: 

## Additional Context
Any other info
```

### Feature Request Template
```markdown
## Feature Description
What is the feature?

## Use Case
Why is this needed?

## Proposed Solution
How should it work?

## Alternative Solutions
Other approaches?

## Additional Context
Any other info
```

## Documentation

### Updating README
- Add your feature to the features list
- Update command examples
- Add configuration if needed

### Adding Examples
- Include working code samples
- Add comments explaining code
- Show expected output

### API Documentation
- Use JSDoc/NatSpec format
- Document parameters and returns
- Include usage examples

## Release Process

Releases follow semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR:** Breaking changes
- **MINOR:** New features (backward compatible)
- **PATCH:** Bug fixes

## Questions?

- Open an issue with the `question` label
- Check existing documentation
- Review closed issues for similar questions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to NOVA COIN! 🚀**
