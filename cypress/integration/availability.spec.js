describe('Test api availability', () => {
  beforeEach(cy.mockAuth)

  const screenshotFolderName = 'test_page_availability'

  it('can reach the backend', () => {
    cy.visitAPI()
    cy.get("h2.title").first().should('have.text', 'Holocron 1.0.0 OAS3')
    cy.screenshot(`${screenshotFolderName}/can_reach_api_docs`)
  })
})