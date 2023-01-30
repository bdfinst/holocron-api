const reactComponentUpdateTimeout = 10000
// describe to only test in dev mode

const setUp = (organizationName, valueStreamName) =>
  cy.apiCreateOrganization(organizationName).then(({ organization }) => {
    cy.apiCreateValueStream(valueStreamName, organization.id).then(
      ({ valuestream }) => {
        cy.wrap({
          organization,
          valuestream,
        })
      },
    )
  })

const tearDown = (createdTeamId, organization, valueStream) => {
    cy.apiDeleteTeam(createdTeamId).then(() => {
      cy.apiDeleteValueStream(valueStream.id).then(() => {
        cy.apiDeleteOrganization(organization.id)
      })
    })
}

describe('Test team CRUD', () => {
  const screenshotFolderName = 'test_team_crud'

  let dummyOrganization,
    dummyValueStream,
    createdTeamId,
    teamName,
    orgName,
    vsName

  beforeEach(cy.mockAuth)

  after(() => {
    tearDown(createdTeamId, dummyOrganization, dummyValueStream)
  })

  before(() => {
    teamName = cy.utils.randomName(8)
    orgName = cy.utils.randomName(8)
    vsName = cy.utils.randomName(8)

    setUp(orgName, vsName).then(({ organization, valuestream }) => {
      dummyOrganization = organization
      dummyValueStream = valuestream
    })
  })

  it('can create a team', () => {
    // visit the create team page first
    cy.visitAddTeamPage()
    // fill out the form
    cy.get(`[id="select-organization"]`).type(`${orgName}{downarrow}{enter}`)
    cy.get(`[id="select-valuestream"]`).type(`${vsName}{downarrow}{enter}`)
    cy.get(`[id="enter-your-team-name"]`).type(teamName)
    cy.get(`[id="enter-the-number-of-members-in-your-team"]`).type('1')
    cy.pickOptionMUIAutocomplete(`[id="select-team-admins"]`)
    cy.pickOptionMUIAutocomplete(`[id="select-ticket-boards"]`)

    cy.screenshot(`${screenshotFolderName}/can_create_a_team_pending`)

    // submit, wait for request fo finish and assert that team was created
    cy.intercept('POST', '**/api/v1/teams').as('createTeam')
    cy.get('form').submit()
    cy.wait('@createTeam')
      .then(({ response }) => {
        const { body } = response
        const { id: teamId } = body
        createdTeamId = teamId
      })
      .its('response.statusCode')
      .should('eq', 201)
    
    cy.waitForAPIDataAfterUserChange()
    // the update and delete button for the team should be visible if the team is created
    cy.get(`[aria-label="update-team-${teamName}"]`, {
      timeout: reactComponentUpdateTimeout,
    })
    cy.get(`[aria-label="delete-team-${teamName}"]`, {
      timeout: reactComponentUpdateTimeout,
    })

    cy.screenshot(`${screenshotFolderName}/can_create_a_team_done`)
  })

  it('can update a team', () => {
    cy.visitUpdateTeamPage(teamName)
    cy.get(`[id="update-the-number-of-members-in-your-team"]`).type(
      '{backspace}2',
    )

    cy.screenshot(`${screenshotFolderName}/can_update_a_team_pending`)

    // submit, wait for request to finish and assert the team was updated
    cy.intercept('PUT', `**/api/v1/teams/${createdTeamId}`).as('updateTeam')
    cy.get('form').submit()
    cy.wait('@updateTeam')
      .its('response.statusCode')
      .should('eq', 200)
      
    cy.waitForAPIDataAfterUserChange()
    cy.get('[aria-label="Search team by name"]').type(teamName)
    cy.get(`[aria-label="update-team-${teamName}"]`).click()
    cy.get(`[id="update-the-number-of-members-in-your-team"]`)
      .should('have.value', '2', { timeout: reactComponentUpdateTimeout })

    cy.screenshot(`${screenshotFolderName}/can_update_a_team_done`)
  })

  it('can delete a team', () => {
    cy.visitAdminPage()
    cy.get('[aria-label="Search team by name"]').type(teamName)
    cy.get(`[aria-label="delete-team-${teamName}"]`).click()
    cy.get(`[aria-labelledby="confirm-dialog"]`).should('exist')
    cy.get(`[aria-label="Enter ${teamName} to Confirm Action"]`).type(
      teamName,
      {
        force: true,
      },
    )

    cy.screenshot(`${screenshotFolderName}/can_delete_a_team_pending`)

    cy.intercept('DELETE', `**/api/v1/teams/${createdTeamId}`).as('deleteTeam')
    cy.get(`[aria-label="Yes Button"]`).click({ force: true })
    cy.wait('@deleteTeam')
      .its('response.statusCode')
      .should('eq', 204)

    cy.waitForAPIDataAfterUserChange()
    cy.get(`[aria-labelledby="confirm-dialog"]`).should('not.exist')
    cy.get(`[aria-label="delete-team-${teamName}"]`).should('not.exist')

    cy.screenshot(`${screenshotFolderName}/can_delete_a_team_done`)
  })
})
